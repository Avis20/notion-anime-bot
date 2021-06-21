import os

import logging.config
import notion
from aiogram import Bot, Dispatcher, types, executor, md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from aiogram.dispatcher import FSMContext
from pathlib import Path
import utils
from aiogram.dispatcher.filters import Text

logging.config.fileConfig(fname=Path.home() / 'develop/notion-bot/' / 'logging.conf', disable_existing_loggers=False)
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


@dp.message_handler()
@dp.message_handler(state='*', commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('Поиск', 'search'),
        ('Создать страницу', 'create_page'),
        ('Отмена', 'cancel'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    await message.reply("Notion bot приветствует тебя\nКакую команду хочешь выполнить?", reply_markup=keyboard_markup)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.search)
# @dp.message_handler()
async def process_name(message: types.Message, state: FSMContext):
    # await state.finish()
    async with state.proxy() as data:
        data['text'] = message.text
    result, error = notion.search(message.text)
    if error:
        return await message.reply(error)

    if result.get('results'):
        count = len(result.get('results'))
        text = md.text(f'<b>Найдено:</b>{count} записей\n\n')
        for item in result.get('results'):
            # ID
            id = item.get('id', '').replace('-', '')
            parent_type = item.get('parent', {})['type']
            parent_id = item.get('parent', {})[parent_type].replace('-', '')
            page_url = f"{config.get('notion', 'host')}/{parent_id}?p={id}"
            text += md.text(f'<b>ID:</b> <a href="{page_url}">{item.get("id")}</a>', '\n')

            prop = item.get('properties', {})

            text += md.text('<b>Название:</b>', prop.get('Name', {}).get('title', [])[0]['text']['content'], '\n')
            text += md.text('<b>Категория:</b>', prop.get('Category', {}).get('multi_select', [{}])[0].get('name'), '\n')
            text += md.text('<b>Статус:</b>', prop.get('Status', {}).get('select', {}).get('name'), '\n')
            if prop.get('url'):
                text += md.text('<b>Смотреть:</b>', prop.get('url', {}).get('url', {}), '\n')
            else:
                text += '\n'
            text += '\n'

        await message.reply(text, parse_mode='HTML')
    else:
        await message.reply(f"По запросу [{message.text}] ничего не найдено")


@dp.message_handler(state=Form.create_page)
# @dp.message_handler()
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['text'] = message.text
    result, error = notion.create_page(message.text)
    if error:
        return await message.reply(error)

    if result.get('id'):
        # ID
        text = ''
        id = result.get('id', '').replace('-', '')
        parent_type = result.get('parent', {})['type']
        parent_id = result.get('parent', {})[parent_type].replace('-', '')
        page_url = f"{config.get('notion', 'host')}/{parent_id}?p={id}"
        text += md.text(f'<b>ID:</b> <a href="{page_url}">{result.get("id")}</a>', '\n')
        await message.reply(text, parse_mode='HTML')
    else:
        await message.reply("Не удалось создать страницу")


@dp.callback_query_handler(text='search')
@dp.callback_query_handler(text='create_page')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    await query.answer(f'You answered with {answer_data!r}')

    if answer_data == 'search':
        await Form.search.set()
        await bot.send_message(query.from_user.id, 'Введите фразу для поиска')
    elif answer_data == 'create_page':
        await Form.create_page.set()
        await bot.send_message(query.from_user.id, 'Введите название страницы')
    else:
        text = f'Unexpected callback data {answer_data!r}!'


if __name__ == '__main__':
    executor.start_polling(dp)
