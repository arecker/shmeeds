"""fetch latest journal entry"""
import argparse
import collections
import json
import os

import feedparser

from shmeeds import logger

_cache = None


def make_parser(parser=None):
    parser = parser or argparse.ArgumentParser('latest')
    parser.add_argument('--feed-url', type=str, help='RSS feed URL', default='https://www.alexrecker.com/feed.xml')
    return parser


def fetch(feed_url):
    global _cache
    if _cache:
        logger.debug('returning cached response %s', feed_url)
        return _cache

    logger.info('fetching RSS feed at %s', feed_url)
    feed = feedparser.parse(feed_url)
    latest = feed.entries[0]
    _cache = collections.OrderedDict(
        bannerURL=latest['media_thumbnail'][0]['url'],
        permalink=latest['link'],
        subtitle=latest['content'][-1]['value'],
        title=latest['title']
    )
    return _cache


def main(args):
    logger.debug('calling `latest` with args %s', args)
    response = fetch(args.feed_url)
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main(make_parser().parse_args())
