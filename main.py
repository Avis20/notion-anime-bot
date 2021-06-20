import os

import logging.config
import notion
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes

import utils

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

config = utils.get_config()
TOKEN = config.get('telegram', 'bot_token')

bot = None
if not os.environ.get('PROXY_OFF'):
    PROXY_URL = config.get('site', 'proxy_host')
    bot = Bot(token=TOKEN, proxy=PROXY_URL)
else:
    bot = Bot(token=TOKEN)

dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware(logger=logger))


@dp.message_handler(content_types=ContentTypes.TEXT)
async def echo_msg(message: types.message):
    result = notion.search(message.text)
    await message.reply(result.get('results')[0].get('id'))


if __name__ == '__main__':
    executor.start_polling(dp)
