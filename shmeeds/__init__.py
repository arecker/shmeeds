__version__ = '0.1.0'

import argparse as _argparse
import logging as _logging
import platform as _platform
import sys as _sys


def _logger(level=_logging.INFO):
    logger = _logging.getLogger('shmeeds')
    logger.setLevel(level=level)
    handler = _logging.StreamHandler(stream=_sys.stderr)
    formatter = _logging.Formatter('SHMEEDS :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = _logger()


def new_parser(name=''):
    parser = _argparse.ArgumentParser(prog=name)
    parser.add_argument('-V', '--version', action='store_true', default=False, help='print version and exit')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='enable verbose logs')
    parser.add_argument('-s', '--silent', action='store_true', default=False, help='hide logs')
    return parser


def print_version_and_exit():
    logger.info(
        'shmeeds = %s, python = %s',
        __version__,
        _platform.python_version()
    )
    _sys.exit()
