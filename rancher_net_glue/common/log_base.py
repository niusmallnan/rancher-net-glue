from __future__ import absolute_import, print_function

import logging
from argparse import Action


LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


class SetLogLevel(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        level = values.upper()
        if level not in LOG_LEVELS:
            raise ValueError("Invalid log level: {0}. Must be one of {1}"
                             .format(values, LOG_LEVELS))
        logging.getLogger('neutron_glue').setLevel(LOG_LEVELS[level])

