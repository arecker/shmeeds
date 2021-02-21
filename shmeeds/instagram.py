from shmeeds.log import logger


def post(response, creds={}, dry=False):
    logger.info('authenticating to instagram')
