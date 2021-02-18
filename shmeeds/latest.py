from shmeeds import logger, new_parser, print_version_and_exit


def main():
    args = new_parser(name='latest').parse_args()
    if args.version:
        print_version_and_exit()

    logger.info('args: %s', args)
    logger.debug('this is a debug message')
    logger.info('this is an info message')
    logger.error('this is an error message')
    try:
        int('fart')
    except ValueError:
        logger.exception('fart is not a number!')
    logger.critical('oh the humanity!!!')


if __name__ == '__main__':
    main()
