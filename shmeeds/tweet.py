"""tweet latest journal entry"""
import argparse
import collections
import json
import os

import feedparser

from shmeeds import logger, latest


def make_parser(parser=None):
    parser = parser or argparse.ArgumentParser('tweet')
    for key in ('access-token', 'access-token-secret', 'consumer-api-key', 'consumer-api-secret-key'):
        parser.add_argument(f'--{key}', type=str, help=f'twitter {key.replace("-", " ")}', required=True)
    return latest.make_parser(parser=parser)


def tweet(body):
    logger.info('BEGIN TWEET\n%s\nEND TWEET', body)


def main(args):
    logger.debug('calling `tweet` with args %s', args)
    response = latest.fetch(args.feed_url)
    body = f'''
{response['title']}
{response['subtitle']}
{response['permalink']}
    '''.strip()
    tweet(body)


if __name__ == '__main__':
    main(make_parser().parse_args())
