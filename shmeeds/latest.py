"""fetch latest journal entry"""
import argparse
import collections
import json
import os

import feedparser

from shmeeds import logger


def make_parser(parser=None):
    parser = parser or argparse.ArgumentParser('latest')


def fetch(feed_url):
    logger.info('fetching RSS feed at %s', feed_url)
    feed = feedparser.parse(feed_url)
    latest = feed.entries[0]
    return collections.OrderedDict(
        bannerURL=latest['media_thumbnail'][0]['url'],
        permalink=latest['link'],
        subtitle=latest['content'][-1]['value'],
        title=latest['title']
    )


def main(args):
    logger.debug('calling `latest` with args %s', args)
    feed_url = os.path.join(args.url, 'feed.xml')
    response = fetch(feed_url)
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main(make_parser().parse_args())
