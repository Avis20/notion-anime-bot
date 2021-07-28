
import os
import configparser
from pathlib import Path

import sys

"""
def check_run_script():
    pid = str(os.getpid())
    pid_file = Path(Path.home() / 'develop/notion-bot/' / '.notion.pid')
    if pid_file.exists():
        logging.error(f"Script is already running! see {pid_file}")
        sys.exit()
"""

def get_config():
    config = configparser.ConfigParser()
    config.read(Path.home() / 'develop/notion-bot/' / 'config.ini')
    return config


if __name__ == '__main__':
    config = get_config()
    print(config)
    print(config.get('telegram', 'bot_token'))
