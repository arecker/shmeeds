"""fetch latest journal entry"""
import argparse

from shmeeds import logger


def make_parser(parser=None):
    parser = parser or argparse.ArgumentParser('latest')


def main(args):
    logger.debug('calling `latest` with args %s', args)


if __name__ == '__main__':
    main(make_parser().parse_args())
