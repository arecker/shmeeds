import argparse
import os
import platform
import sys

from shmeeds import log, __version__, config, tweet, latest
from shmeeds.log import logger


parser = argparse.ArgumentParser(prog='shmeeds')
log_opts = parser.add_mutually_exclusive_group()
log_opts.add_argument('-v', '--verbose', action='store_true', default=False, help='show debug logs')
log_opts.add_argument('-s', '--silent', action='store_true', default=False, help='hide all logs')

parser.add_argument('-C', '--config', type=str, default=config.default_path, help='path to config file')
parser.add_argument('--dry', action='store_true', default=False, help='stub out API calls')
parser.add_argument('--feed-url', type=str, default='https://www.alexrecker.com/feed.xml', help='RSS feed url')


def main():
    args = parser.parse_args()

    if args.silent:
        log.disable_logger()
    elif args.verbose:
        log.enable_verbose()

    logger.debug('shmeeds = %s, python = %s (%s)', __version__, platform.python_version(), sys.executable)

    if os.path.exists(args.config):
        config.load(args.config)
    else:
        logger.error('config file "%s" does not exist!')
        sys.exit(1)

    response = latest.fetch(args.feed_url)

    if config.twitter():
        tweet.tweet(response, creds=config.twitter(), dry=args.dry)
