from __future__ import absolute_import, print_function

import logging
from argparse import ArgumentParser

from .handler import RancherConnector
from .neutron import PortUpdateExecutor
from rancher_net_glue.common.cli_base import validate_rancher_args, add_ranche_args
from rancher_net_glue.common.log_base import SetLogLevel, LOG_LEVELS

logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser('neutron-glue', add_help=False,
                            description="Rancher net glue for OpenStack Neutron")

    rancher_args = parser.add_argument_group('rancher arguments')
    add_ranche_args(rancher_args)

    neutron_args = parser.add_argument_group('neutron arguments')
    neutron_args.add_argument('--keystone-url', help='Keystone Auth URL')
    neutron_args.add_argument('--tenant-name', help='Tenant/Project Name')
    neutron_args.add_argument('--username', help='User Name')
    neutron_args.add_argument('--password', help='User password')

    optional_args = parser.add_argument_group('optional arguments')
    optional_args.add_argument("-h", "--help", action="help",
                               help="show this help message and exit")
    optional_args.add_argument('--log-level', action=SetLogLevel,
                               default='INFO', choices=LOG_LEVELS,
                               help='Set the log level.')

    args = parser.parse_args()
    if not validate_rancher_args(args):
        return

    try:
        job_executor = PortUpdateExecutor()
        job_executor.initialize(args.keystone_url, args.username,
                                args.password, args.tenant_name)

        rancher_url = args.rancher_url
        if rancher_url.endswith('/'):
            rancher_url = args.rancher_url[:-1]
        handler = RancherConnector(rancher_url, args.project_id,
                                   args.access_key, args.secret_key,
                                   job_executor)
        handler()
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
