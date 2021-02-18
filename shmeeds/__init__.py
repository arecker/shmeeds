__version__ = '0.1.0'

import argparse as _argparse
import logging as _logging
import sys as _sys


def new_logger(level=_logging.INFO):
    logger = _logging.getLogger('shmeeds')
    logger.setLevel(level=level)
    handler = _logging.StreamHandler(stream=_sys.stderr)
    formatter = _logging.Formatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def new_parser():
    parser = _argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug logs')
    parser.add_argument('-s', '--silent', action='store_true', default=False, help='hide logs')
    return parser
