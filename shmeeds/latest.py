"""fetch latest journal entry"""
import collections

import feedparser

from shmeeds.log import logger


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
