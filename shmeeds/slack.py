import copy
import json

import requests

from shmeeds.log import logger


def post(response, config, dry=False):
    url = config.pop('webhook')

    text = f'''
{response['title']}
{response['subtitle']}
{response['permalink']}
    '''.strip()

    data = copy.copy(config)
    data.update({'text': text})
    headers = {'Content-Type': 'application/json'}

    logger.debug('BEGIN SLACK\n%s\nEND SLACK', text)

    if not dry:
        requests.post(url, headers=headers, data=json.dumps(data)).raise_for_status()
