from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, code, italic, text
from config import TOKEN

from database.media_app.models import MediaIds

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        'Привет!\nИспользуй /help, чтобы узнать список доступных команд'
    )


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(
        bold('Команды'),
        '/voice',
        '/photo',
        '/group',
        '/note',
        '/file',
        '/testpre',
        sep='\n'
    )
    await message.reply(
        msg, parse_mode=ParseMode.MARKDOWN
    )


@dp.message_handler(commands=['voice'])
async def send_first_love_story(message: types.Message):
    voice = await MediaIds.objects.aget(filename__icontains='first love story')
    await bot.send_voice(
        message.from_user.id,
        voice=voice,
        caption='my first love story'
    )


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize('Я не знаю, что с этим делать :astonished:'),
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
