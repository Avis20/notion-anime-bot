import logging
import os
from logging import handlers

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from flask import Flask

import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
log_handler = handlers.RotatingFileHandler(utils.get_log_name(), maxBytes=5*1024, backupCount=2)
logger.addHandler(log_handler)

config = utils.get_config()
TOKEN = config.get('telegram', 'bot_token')
WEBHOOK_HOST = config.get('site', 'webhook_host')
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = config.get('site', 'webhook_port')

bot = None
if not os.environ.get('PROXY_OFF'):
    PROXY_URL = config.get('site', 'proxy_host')
    bot = Bot(token=TOKEN, proxy=PROXY_URL)
else:
    bot = Bot(token=TOKEN)

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)


@app.route('/')
def echo():
    return 'hello'


@dp.message_handler()
async def echo(message: types.Message):
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    app.run()