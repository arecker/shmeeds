import logging
import sys


def make_logger(level=logging.INFO):
    logger = logging.getLogger('shmeeds')
    logger.setLevel(level=level)
    handler = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter('SHMEEDS :: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = make_logger()


def disable_logger():
    logger.disabled = True


def enable_verbose():
    logger.setLevel(level=logging.DEBUG)
