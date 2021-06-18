import os
import configparser
from pathlib import Path

# BOT_TOKEN = os.environ.get('BOT_TOKEN')


def get_log_name():
    log_dir = Path.home() / 'logs'
    if not log_dir.exists():
        os.makedirs(log_dir)
    return log_dir / 'notion-tg-bot.log'


def get_config():
    config = configparser.ConfigParser()
    # config.read(Path.home() / 'mysite' / '.config')
    config.read(Path.cwd() / '.config')
    return config


if __name__ == '__main__':
    config = get_config()
    print(config)
    print(config.get('telegram', 'BOT_TOKEN'))
