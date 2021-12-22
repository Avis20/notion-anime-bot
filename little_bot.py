import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

import utils
import nlogger

logger = nlogger.get_logger()
config = utils.get_config()
TOKEN = config.get('telegram', 'bot_token')
bot = Bot(token=TOKEN)

# webhook settings
WEBHOOK_HOST = config.get('telegram', 'webhook_host')
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = config.get('app', 'webapp_port')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger=logger))

#
# @dp.message_handler(commands='test')
# async def echo_if_test(message: types.Message):
#     return SendMessage(message.chat.id, 'FFFFF')


# '''
# echo ответ на любое сообщение
@dp.message_handler()
async def echo(message: types.Message):
    return SendMessage(message.chat.id, message.text)
# '''


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
