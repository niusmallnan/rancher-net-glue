from __future__ import absolute_import

import requests
import logging

logger = logging.getLogger(__name__)


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

    def get_running_instances(self):
        url = '{0}/v2-beta/projects/{1}/instances?state=running'\
            .format(self.url, self.project_id)
        res = requests.get(url, headers=self._headers)
        res_data = res.json()
        if res_data['data'] and len(res_data['data']) > 0:
            return res_data['data']
        return None

    def get_host(self, host_id):
        url = '{0}/v2-beta/projects/{1}/hosts/{2}'\
            .format(self.url, self.project_id, host_id)
        res = requests.get(url, headers=self._headers)
        return res.json()

    def get_instances_by_host(self, host_id):
        url = '{0}/v2-beta/projects/{1}/hosts/{2}/instances?state=running'\
            .format(self.url, self.project_id, host_id)
        res = requests.get(url, headers=self._headers)
        res_data = res.json()
        if res_data['data'] and len(res_data['data']) > 0:
            return res_data['data']
        return None

