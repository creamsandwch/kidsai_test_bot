from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor
from emoji import emojize
from aiogram.utils.markdown import bold, code, italic, text
from config import TOKEN, URL
from keyboards import inline_kb
from utils import search_for_file_by_name

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        'Привет!\nИспользуй /help, чтобы узнать список доступных команд',
    )


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(
        bold('Команды: '),
        '/about_me',
        sep='\n'
    )
    await message.reply(
        msg, parse_mode=ParseMode.MARKDOWN
    )


@dp.message_handler(commands=['voices'])
async def process_command_1(message: types.Message):
    await message.reply('История первой любви', reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data == 'love_story')
async def process_callback_lovestory_button(
    callback_query: types.CallbackQuery
):
    await bot.answer_callback_query(callback_query.id)
    json_resp = await search_for_file_by_name(url=URL, filename='love_story.ogg')
    if json_resp:
        telegram_id = json_resp[0].get('file_id')
    else:
        await bot.send_message(
            callback_query.from_user.id,
            text='Файл не был найден на сервере',
        )
    await bot.send_voice(
        callback_query.from_user.id,
        voice=telegram_id,
        caption='История первой любви'
    )


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
