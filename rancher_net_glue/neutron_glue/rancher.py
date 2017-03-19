from __future__ import absolute_import
import requests


class API(object):

    def __init__(self, url, project_id, api_token):
        self.url = url
        self.project_id = project_id
        self.api_token = api_token
        self._headers = {
            'Authorization': 'Basic {0}'.format(api_token)
        }

    def get_active_hosts(self):
        url = '{0}/v2-beta/projects/{1}/hosts?state=active'\
            .format(self.url, self.project_id)
        res = requests.get(url, headers=self._headers)
        res_data = res.json()
        if res_data['data'] and len(res_data['data']) > 0:
            return res_data['data']
        return None

    def get_hosts_neutron_info(self):
        hosts = self.get_active_hosts()
        if hosts:
            neutron_info = {}
            for host in hosts:
                agent_ip = host['agentIpAddress']
                neutron_port_id = host['labels']['io.rancher.neutron.port_id']
                neutron_info[neutron_port_id] = agent_ip
            return neutron_info
        return None

    def get_running_instances(self):
        url = '{0}/v2-beta/projects/{1}/instances'\
            .format(self.rancher_url, self.project_id)
        res = requests.get(url, headers=self._headers)
        res_data = res.json()
        if res_data['data'] and len(res_data['data']) > 0:
            instances = []
            for resource in res_data['data']:
                if resource['state'] == 'running':
                    instances.append(resource['data'])
            return instances
        return None


