from __future__ import absolute_import, print_function

import logging
from argparse import ArgumentParser

from .handler import RancherConnector
from common.cli_base import validate_rancher_args, add_ranche_args
from common.log_base import SetLogLevel, LOG_LEVELS

logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser('neutron-glue', add_help=False,
                            description="Rancher net glue for OpenStack Neutron")

    named_args = parser.add_argument_group('named arguments')
    add_ranche_args(named_args)

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
        if args.rancher_url.endswith('/'):
            rancher_url = args.rancher_url[:-1]
        handler = RancherConnector(rancher_url, args.project_id,
                                   args.access_key, args.secret_key)
        handler()
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
