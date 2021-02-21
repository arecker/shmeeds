import argparse
import os
import platform
import sys

from shmeeds import log, __version__, config, tweet, latest, slack, instagram
from shmeeds.log import logger


parser = argparse.ArgumentParser(prog='shmeeds')
log_opts = parser.add_mutually_exclusive_group()
log_opts.add_argument('-v', '--verbose', action='store_true', default=False, help='show debug logs')
log_opts.add_argument('-s', '--silent', action='store_true', default=False, help='hide all logs')

parser.add_argument('-C', '--config', type=str, default=config.default_path, help='path to config file')
parser.add_argument('--dry', action='store_true', default=False, help='stub out API calls')
parser.add_argument('--wait', action='store_true', default=False, help='wait until latest matches git remote')
parser.add_argument('--feed-url', type=str, default='https://www.alexrecker.com/feed.xml', help='RSS feed url')

github_opts = parser.add_argument_group()
github_opts.add_argument('--github-user', type=str, default='arecker', help='github username')
github_opts.add_argument('--github-repo', type=str, default='blog', help='github repo name')


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

    if args.wait:
        response = latest.wait_for_remote(args.feed_url, user=args.github_user, repo=args.github_repo)
    else:
        response = latest.fetch(args.feed_url)

    if config.twitter():
        tweet.tweet(response, creds=config.twitter(), dry=args.dry)
    else:
        logger.info('no twitter section in config, skipping...')

    if config.instagram():
        instagram.post(response, creds=config.instagram(), dry=args.dry)
    else:
        logger.info('no instagram section in config, skipping...')

    if config.slacks():
        for team, cfg in config.slacks().items():
            logger.info('posting to %s slack workspace', team)
            slack.post(response, cfg, dry=args.dry)
    else:
        logger.info('no slacks configured, skipping...')

    logger.info('done!')
