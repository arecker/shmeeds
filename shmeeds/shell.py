import subprocess

from shmeeds.log import logger


class CommandFailed(Exception):
    pass


def run(cmd, supress_error=False):
    process = subprocess.Popen(
        cmd.split(' '),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if not supress_error and process.returncode != 0:
        raise CommandFailed(f'`{cmd}` failed, returning {process.returncode}')

    logger.debug('command `%s` succeeded', cmd)

    return stdout.decode('utf-8').strip()
