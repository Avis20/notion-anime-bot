import os

from pathlib import Path

BOT_TOKEN = os.environ.get('BOT_TOKEN')


def get_log_name():
    log_dir = Path.home() / 'logs'
    if not log_dir.exists():
        os.makedirs(log_dir)
    return log_dir / 'notion-tg-bot.log'
