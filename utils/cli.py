import argparse
import functools

from config import WebhookConfig, Config
from log import logging_config as log
from log.logging_core import init_logger

try:
    import aiohttp_autoreload
except ImportError:
    aiohttp_autoreload = None

# logger = Logger(__name__)
logger = init_logger()

PROGRAM_DESC = (
    "This program is a Python 3+ script. The script launches a bot in Telegram."
)


# PROGRAM_EP = f"{__copyright__} {__author__} License {__license__}."


def create_parser():
    arg_parser = argparse.ArgumentParser(prog="StudyHUB", description=PROGRAM_DESC)
    arg_parser.add_argument('-p', '--polling', action='store_const', const=True,
                            help="Run tg bot with polling. Default use WebHook")
    arg_parser.add_argument('-a', '--autoreload', action='store_const', const=True,
                            help="Reload application on file changes")
    arg_parser.add_argument('-s', '--skip-updates', action='store_const', const=True,
                            help="Skip pending updates")
    return arg_parser


def cli(config: Config):
    def auto_reload_mixin(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if namespace.autoreload and aiohttp_autoreload:
                logger.warning(
                    "Application started in live-reload mode. Please disable it in production!"
                )
                aiohttp_autoreload.start()
            elif namespace.autoreload and not aiohttp_autoreload:
                logger.warning("`aiohttp_autoreload` is not installed.", err=True)
            return func(*args, **kwargs)

        return wrapper

    @auto_reload_mixin
    def polling(skip_updates: bool):
        """
        Start application
        """
        from utils.executor import runner
        logger.info("starting polling...")

        runner.skip_updates = skip_updates
        runner.start_polling()

    @auto_reload_mixin
    def webhook(webhook_config: WebhookConfig):
        """
        Run application in webhook mode
        """
        from utils.executor import runner
        logger.info("starting webhook...")
        runner.start_webhook(**webhook_config.listener_kwargs)

    log.setup(config)
    parser = create_parser()
    namespace = parser.parse_args()

    import misc

    misc.setup(config)
    polling(True)

'''
    if namespace.polling:
        polling(namespace.skip_updates)
    else:
        webhook(config.webhook)
'''