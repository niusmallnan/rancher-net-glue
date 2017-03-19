from __future__ import absolute_import

import logging

from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client

logger = logging.getLogger(__name__)

CONTAINER_KIND = 'container'
BRIDGE_KIND = 'bridge'
_BRIDGE_MAC_PRE = '00:aa:bb:'


class AddressPair(object):

    def __init__(self, ip, mac, kind=CONTAINER_KIND):
        self.ip = ip
        self.mac = mac
        self.kind = kind

    def __eq__(self, other):
        return (self.ip == other.ip and self.mac == other.mac)

    def json(self):
        return {'ip_address': self.ip, 'mac_address': self.mac}

    def __repr__(self):
        return str(self.json())

class PortUpdate(object):

    def __init__(self, neutron_port_id, address_pairs=[]):
        self.neutron_port_id = neutron_port_id
        self.address_pairs = address_pairs

    def add_address_pair(self, address_pair):
        if address_pair not in self.address_pairs:
            self.address_pairs.append(address_pair)

    def __call__(self, neutron):
        allowed_address_pairs = []
        for ap in self.address_pairs:
            if ap.kind == BRIDGE_KIND:
                port_info = neutron.show_port(self.neutron_port_id)
                port_mac = port_info.mac_address
                ap.mac = _BRIDGE_MAC_PRE + ':'.join(port_mac.split(':')[3:])
            allowed_address_pairs.append(ap.json())
        neutron.update_port(self.neutron_port_id,
                            allowed_address_pairs=allowed_address_pairs)


class PortUpdateExecutor(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(PortUpdateExecutor, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def initialize(self, auth_url, username, password, project_name):
        auth = identity.Password(auth_url=auth_url,
                                 username=username,
                                 password=password,
                                 project_name=project_name)
        sess = session.Session(auth=auth)
        self.neutron = client.Client(session=sess)
        self.port_update_jobs = {}

    def add_job(self, host_id, address_pair, neutron_port_id=None):
        logger.info('host_id: %s, address_pair: %s, neutron_port_id: %s' % (host_id,
                                                                            address_pair,
                                                                            neutron_port_id))
        if self.port_update_jobs.has_key(host_id):
            self.port_update_jobs[host_id].add_address_pair(address_pair)
        else:
            job = PortUpdate(neutron_port_id, [address_pair])
            self.port_update_jobs[host_id] = job

    def execute_all(self):
        for job in self.port_update_jobs.itervalues():
            job()

    def execute_one(self, host_id):
        self.port_update_jobs[host_id]()

