from __future__ import absolute_import


def get_neutron_port_id(host):
    return host['labels']['io.rancher.neutron.port_id']

def get_container_ip(inst):
    return inst['labels']['io.rancher.container.ip']

def get_container_mac(inst):
    return inst['labels']['io.rancher.container.mac_address']

