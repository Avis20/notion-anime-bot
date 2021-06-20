import os

import logging.config
import notion
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from aiogram.dispatcher import FSMContext

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

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger=logger))


class Form(StatesGroup):
    search = State()
    create_page = State()


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('Поиск', 'search'),
        ('Создать страницу', 'create_page'),
        ('Отмена', 'cancel'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    await message.reply("Привет! Notion bot приветствует тебя\nКакую команду хочешь выполнить?", reply_markup=keyboard_markup)


# @dp.message_handler(state=Form.search)
@dp.message_handler()
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search'] = message.text
    result = notion.search(message.text)
    if result.get('results'):
        count = len(result.get('results'))
        text = f'Найдено: {count} записей\n\n'
        for item in result.get('results'):
            text += item['properties']['Name']['title'][0]['text']['content'] + '\n'
            if item['properties'] and item['properties'].get('url'):
                text += 'Смотреть: ' + item['properties'].get('url').get('url') + '\n\n'
            else:
                text += '\n'
        # data = result.get('results')[0]
        # await message.reply(data['properties']['Name']['title'][0]['text']['content'])
        await message.reply(text)
    else:
        await message.reply(f"По запросу [{message.text}] ничего не найдено")


@dp.callback_query_handler(text='search')
@dp.callback_query_handler(text='create_page')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    await query.answer(f'You answered with {answer_data!r}')

    if answer_data == 'search':
        await Form.search.set()
    elif answer_data == 'create_page':
        text = 'Oh no...Why so?'
    else:
        print("\n")
        print('AAAAAAAAAa')
        print("\n")
        text = f'Unexpected callback data {answer_data!r}!'

    await bot.send_message(query.from_user.id, 'Введите фразу для поиска')


if __name__ == '__main__':
    executor.start_polling(dp)
