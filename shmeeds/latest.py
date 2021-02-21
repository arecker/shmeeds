import collections
import datetime
import os
import time

import feedparser
import requests

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


def fetch_latest_from_remote(user, repo):
    url = f'https://api.github.com/repos/{user}/{repo}/git/trees/master?recursive=1'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    paths = [r['path'] for r in data['tree']]
    post_paths = list(filter(lambda p: p.startswith('_posts/'), paths))
    post_slugs = [os.path.basename(p).split('-entry.md')[0] for p in post_paths]
    latest_date = datetime.datetime.strptime(sorted(post_slugs)[-1], '%Y-%m-%d')
    return latest_date.strftime('%A, %B %-d %Y')


def wait_for_remote(feed_url, user='', repo=''):
    logger.info('waiting until feed matches remote')
    latest_on_remote = fetch_latest_from_remote(user, repo)
    latest_on_feed = fetch(feed_url)

    while latest_on_remote != latest_on_feed['title']:
        logger.debug('checking... %s != %s', latest_on_remote, latest_on_feed['title'])
        time.sleep(1)
        latest_on_feed = fetch(feed_url)

    logger.info('%s present in both feed and remote', latest_on_remote)
    return latest_on_feed
