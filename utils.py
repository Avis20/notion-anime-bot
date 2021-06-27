
import os
import configparser
from pathlib import Path
import logging.config

import sys

logging.config.fileConfig(fname=Path.home() / 'develop/notion-bot/' / 'logging.conf')

"""
def check_run_script():
    pid = str(os.getpid())
    pid_file = Path(Path.home() / 'develop/notion-bot/' / '.notion.pid')
    if pid_file.exists():
        logging.error(f"Script is already running! see {pid_file}")
        sys.exit()
"""


def get_log_name():
    log_dir = Path.home() / 'logs'
    if not log_dir.exists():
        os.makedirs(log_dir)
    return log_dir / 'notion-tg-bot.log'


def get_config():
    config = configparser.ConfigParser()
    config.read(Path.home() / 'develop/notion-bot/' / '.config')
    return config


if __name__ == '__main__':
    config = get_config()
    print(config)
    print(config.get('telegram', 'bot_token'))
