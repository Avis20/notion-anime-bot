
import logging
import logging.handlers as handlers

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes

import utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
log_handler = handlers.RotatingFileHandler(utils.get_log_name(), maxBytes=5*1024, backupCount=2)
logger.addHandler(log_handler)


TOKEN = utils.BOT_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware(logger=logger))


@dp.message_handler(content_types=ContentTypes.TEXT)
async def echo_msg(message: types.message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
