import InstagramAPI

from shmeeds.log import logger


def post(response, creds={}, dry=False):
    logger.info('sharing story to instagram')
