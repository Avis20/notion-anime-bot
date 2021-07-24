
import os
import logging.config
from pathlib import Path

log_config_path = Path.home() / 'develop/notion-bot/nlogger/' / 'logging.conf'
log_dir = Path.home() / 'develop/notion-bot/logs/'


def get_logger():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.config.fileConfig(fname=log_config_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)
