from __future__ import absolute_import


def get_neutron_port_id(host):
    return host['labels']['io.rancher.neutron.port_id']

def get_container_ip(inst):
    if inst['labels'].has_key('io.rancher.container.ip'):
        return inst['labels']['io.rancher.container.ip']
    return None

def get_container_mac(inst):
    if inst['labels'].has_key('io.rancher.container.mac_address'):
        return inst['labels']['io.rancher.container.mac_address']
    return None
