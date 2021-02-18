from shmeeds import new_logger, new_parser


def main():
    logger = new_logger()
    args = new_parser().parse_args()
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
