"""tweet latest journal entry"""
import tweepy

from shmeeds.log import logger


def make_client(creds):
    auth = tweepy.OAuthHandler(creds['consumer_api_key'], creds['consumer_api_secret_key'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])
    return tweepy.API(auth)


def response_to_status(response):
    return f'''
{response['title']}
{response['subtitle']}
{response['permalink']}
    '''.strip()


def tweet(response, creds=None, dry=False):
    status = response_to_status(response)
    logger.info('posting tweet for %s', response['title'])
    logger.debug('BEGIN TWEET\n%s\nEND TWEET', status)
    client = make_client(creds)
    if not dry:
        client.update_status(status)
