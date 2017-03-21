from __future__ import absolute_import

import json
import logging
import websocket

from threading import Thread

from rancher_net_glue.neutron_glue import util
from .compat import b64encode
from .rancher import API
from .neutron import AddressPair, BRIDGE_KIND

logger = logging.getLogger(__name__)

# Change the log level on the requests library
logging.getLogger("requests").setLevel(logging.WARNING)


class RancherConnector(object):

    def __init__(self, rancher_url, project_id, access_key, secret_key, job_executor):
        self.rancher_url = rancher_url
        self.project_id = project_id
        self.api_token = b64encode("{0}:{1}".format(access_key, secret_key))

        self.job_executor = job_executor

    def __call__(self):
        self._start_reload()
        self.start()

    def _start_reload(self):
        api = API(self.rancher_url, self.project_id, self.api_token)
        hosts = api.get_active_hosts()
        if hosts:
            for host in hosts:
                logger.debug('host: %s' % host)
                host_id = host['id']
                agent_ip = host['agentIpAddress']
                neutron_port_id = util.get_neutron_port_id(host)
                ap = AddressPair(agent_ip, None, BRIDGE_KIND)
                self.job_executor.add_job(host_id, ap, neutron_port_id)

        instances = api.get_running_instances()
        if instances:
            for inst in instances:
                logger.debug('instance: %s' % inst)
                host_id = inst['hostId']
                ip = util.get_container_ip(inst)
                mac = util.get_container_mac(inst)
                ap = AddressPair(ip, mac)
                self.job_executor.add_job(host_id, ap)

        self.job_executor.execute_all()

    def start(self):
        header = {
            'Authorization': 'Basic {0}'.format(self.api_token)
        }
        websocket_url = self.rancher_url.replace('http', 'ws')
        url = '{0}/v2-beta/projects/{1}/subscribe?eventNames='\
            'resource.change'\
            .format(websocket_url, self.project_id)
        self.ws = websocket.WebSocketApp(url, header=header,
                                         on_message=self._on_message,
                                         on_open=self._on_open,
                                         on_error=self._on_error,
                                         on_close=self._on_close)

        logger.info('Watching for rancher events')
        self.ws.run_forever()

    def _on_open(self, ws):  # pragma: no cover
        logger.info("Websocket connection open")

    def _on_close(self, ws):  # pragma: no cover
        logger.info('Websocket connection closed')

    def _on_error(self, ws, error):  # pragma: no cover
        logger.error(error)

    def _on_message(self, ws, message):
        msg = json.loads(message)
        if msg['name'] == 'resource.change' and msg['data']:
            handler = MessageHandler(msg, self.rancher_url,
                                     self.project_id, self.api_token,
                                     job_executor=self.job_executor)
            handler.start()


class MessageHandler(Thread):
    def __init__(self, message, rancher_url, project_id, api_token,
                 job_executor):
        Thread.__init__(self)
        self.message = message
        self.rancher_url = rancher_url
        self.project_id = project_id
        self.api_token = api_token
        self.job_executor = job_executor

    def run(self):
        resource = self.message['data']['resource']
        logger.info('rancher events resource: %s' % resource)
        if resource['type'] == 'container' and \
                resource['state'] in ['running', 'stopped']:
            host_id = resource['hostId']
            api = API(self.rancher_url, self.project_id, self.api_token)
            host = api.get_host(host_id)
            agent_ip = host['agentIpAddress']
            neutron_port_id = util.get_neutron_port_id(host)
            host_ap = AddressPair(agent_ip, None, BRIDGE_KIND)
            self.job_executor.add_job(host_id, host_ap, neutron_port_id)

            instances = api.get_instances_by_host(host_id)
            for inst in instances:
                ip = util.get_container_ip(inst)
                mac = util.get_container_mac(inst)
                ap = AddressPair(ip, mac)
                self.job_executor.add_job(host_id, ap)

            self.job_executor.execute_one(host_id)

