__version__ = '0.1.0'

import argparse as _argparse
import importlib as _importlib
import logging as _logging
import platform as _platform
import sys as _sys


def _make_logger(level=_logging.INFO):
    logger = _logging.getLogger('shmeeds')
    logger.setLevel(level=level)
    handler = _logging.StreamHandler(stream=_sys.stderr)
    formatter = _logging.Formatter('SHMEEDS :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = _make_logger()


def make_parser():
    parser = _argparse.ArgumentParser(prog='shmeeds')

    # global options
    parser.add_argument('--url', type=str, help='blog URL', default='https://www.alexrecker.com')
    log_opts = parser.add_mutually_exclusive_group()
    log_opts.add_argument('-v', '--verbose', action='store_true', default=False, help='show debug logs')
    log_opts.add_argument('-s', '--silent', action='store_true', default=False, help='hide all logs')

    # subcommands
    subcommands = ('latest', )
    subparsers = parser.add_subparsers(dest='command', required=True)
    for cmd in subcommands:
        logger.debug('creating subparser for %s subcommand', cmd)
        lib = _importlib.import_module(f'shmeeds.{cmd}')
        subparser = subparsers.add_parser(cmd, help=lib.__doc__)
        lib.make_parser(parser=subparser)

    return parser


def main(args=None):
    args = args or make_parser().parse_args()

    if args.silent:
        logger.propagate = False
    elif args.verbose:
        logger.setLevel(level=_logging.DEBUG)

    logger.debug(
        'shmeeds = %s, python = %s (%s)',
        __version__,
        _platform.python_version(),
        _sys.executable
    )

    _importlib.import_module(f'shmeeds.{args.command}').main(args)


if __name__ == '__main__':
    main(make_parser().parse_args())
