import configparser
import os

from shmeeds.log import logger
from shmeeds import shell


default_path = os.path.expanduser('~/.shmeeds.conf')


data = configparser.ConfigParser()


def load(path):
    global data

    logger.info('loading config file from %s', path)
    data.read(path)

    sections = data.sections()
    logger.debug('found config sections %s', sections)

    for section in sections:
        logger.debug('evaluating section %s', section)
        for option, value in data.items(section):
            new_option, new_value = None, None
            if option.endswith('_cmd'):
                new_option, _ = option.split('_cmd')
                new_value = shell.run(value)
            elif option.endswith('_env'):
                new_option, _ = option.split('_env')
                new_value = os.environ[value]
            if all([new_option, new_value]):
                logger.debug('expanding command %s:%s -> %s:%s', section, option, section, new_option)
                data.remove_option(section, option)
                data.set(section, new_option, new_value)


def twitter():
    global data
    try:
        return dict(data.items('twitter', {}))
    except configparser.NoSectionError:
        logger.info('no twitter section in config, skipping...')


def slacks():
    global data
    slack_sections = [s for s in data.sections() if s.startswith('slack:')]
    aggregate = {}
    for section in slack_sections:
        _, key = section.split('slack:')
        aggregate[key] = dict(data.items(section))
    return aggregate
