
import logging
import logging.handlers as handlers
import uuid

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes
from aiogram.utils.executor import start_webhook

import utils

# webhook settings
WEBHOOK_HOST = 'https://yorlov.pythonanywhere.com'
WEBHOOK_PATH = f'/path/to/api/{uuid.uuid4()}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 3001

# logger
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
