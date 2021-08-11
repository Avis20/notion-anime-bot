from aiogram import Bot, Dispatcher, types, md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook

import nlogger
from model import notion_model
import utils
import anime_parser

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
WEBAPP_PORT = config.get('telegram', 'webapp_port')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger=logger))


class Form(StatesGroup):
    search = State()
    create_page = State()


# Убить процесс
'''
@dp.message_handler(state=Form.kill)
async def kill_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Процесс остановлен")
    sys.exit()
'''


'''
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state=)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())
'''


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


# @dp.message_handler()
@dp.message_handler(state=Form.search)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['text'] = message.text
    result, error = notion_model.search_page(message.text)
    if error:
        return await message.reply(error)

    if not result.get('results'):
        return await message.reply(f"По запросу [{message.text}] ничего не найдено")

    count = len(result.get('results'))
    text = md.text(f'<b>Найдено:</b>{count} записей\n\n')
    for item in result.get('results'):
        # ID
        id = item.get('id', '').replace('-', '')

        database_id = config.get('notion', 'database_id')
        page_url = f"{config.get('notion', 'host')}/{database_id}?p={id}"

        text += md.text(f'<b>ID:</b> <a href="{page_url}">{id}</a>', '\n')
        text += md.text('<b>Название:</b>', item.get('title', {}), '\n')
        text += md.text('<b>Категория:</b>', item.get('categories', {}), '\n')
        text += md.text('<b>Статус:</b>', item.get('name'), '\n')
        text += md.text('<b>Смотреть:</b>', item.get('url', {}), '\n')
        text += '\n'
    await message.reply(text, parse_mode='HTML')


@dp.message_handler(state=Form.create_page)
# @dp.message_handler()
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['text'] = message.text
    find_data = anime_parser.search_data(message.text)
    result, error = notion_model.create_page(find_data)
    if error:
        return await message.reply(error)

    if result.get('id'):
        # ID
        text = ''
        id = result.get('id', '').replace('-', '')
        database_id = config.get('notion', 'database_id')
        page_url = f"{config.get('notion', 'host')}/{database_id}?p={id}"
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


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logger.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.warning('Bye!')


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
