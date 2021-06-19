import logging
import os
from logging import handlers

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes

from flask import Flask

import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
log_handler = handlers.RotatingFileHandler(utils.get_log_name(), maxBytes=5*1024, backupCount=2)
logger.addHandler(log_handler)

config = utils.get_config()
TOKEN = config.get('telegram', 'bot_token')

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


@dp.message_handler(content_types=ContentTypes.TEXT)
async def echo_msg(message: types.message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
    app.run()