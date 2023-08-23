import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram.utils.markdown import bold, code, italic, text
from config import TOKEN, URL, MEDIA_PATH, ABOUT_POST, REPO_URL, \
    BOT_DIR
from keyboards import voices_inline_kb, photos_inline_kb
from utils import search_for_file_by_name
from stt import voice_to_text

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


logging.basicConfig(
    format=(
        '%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s'
        ' [%(asctime)s]  %(message)s'
    ),
    level=logging.INFO
)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """Text message on start command."""
    await message.reply(
        'Привет!\nИспользуй /help, чтобы узнать список доступных команд',
    )


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    """Text message containing all available text commands."""
    msg = text(
        bold('Команды:'),
        '/photos - мои фото',
        '/voices - мои голосовые с короткими рассказами',
        '/about - про моё главное увлечение',
        '/repo - ссылка на репозиторий с исходниками этого бота',
        sep='\n'
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=msg, parse_mode=ParseMode.MARKDOWN
    )


@dp.message_handler(commands=['photos'])
async def process_command_photos(message: types.Message):
    """Shows inline keyboard with photo message options."""
    await message.reply('Мои фото', reply_markup=photos_inline_kb)


@dp.message_handler(commands=['voices'])
async def process_command_voices(message: types.Message):
    """Shows inline keyboard with voice message options."""
    await message.reply('Голосовые сообщения', reply_markup=voices_inline_kb)


async def get_file_id(filename=None):
    """
    Searches for filename on GET to media_ids/.
    Basically - in django media/ folder.
    """
    logging.info('searching for {} in {}'.format(filename, MEDIA_PATH))
    json_resp = await search_for_file_by_name(url=URL, filename=filename)
    if not json_resp:
        return None
    else:
        return json_resp[0].get('file_id')


@dp.callback_query_handler(lambda c: c.data.startswith('voicebtn'))
async def process_callback_voices_buttons(
    callback_query: types.CallbackQuery
):
    """
    Catches keyboard buttons starting with voicebtn_ and
    sends voices found in database by filename: {filename}.ogg
    """
    command = callback_query.data
    filename = command.replace('voicebtn_', '') + '.ogg'
    file_id = await get_file_id(filename=filename)
    if not file_id:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text=f'Файл {filename} не был найден в media/voice/'
        )
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_voice(
            callback_query.from_user.id,
            voice=file_id,
        )


@dp.callback_query_handler(lambda c: c.data.startswith('photobtn'))
async def process_callback_photos_button(
    callback_query: types.CallbackQuery
):
    """
    Catches keyboard buttons starting with photobtn
    and sends photos found in database by filename: {filename.jpg}.
    """
    filename = callback_query.data.replace('photobtn_', '') + '.jpg'
    file_id = await get_file_id(filename=filename)
    if not file_id:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            text=f'Файл {filename} не был найден в media/photo/'
        )
    else:
        await bot.answer_callback_query(callback_query.id)
        caption = ''
        if 'highschool' in filename:
            caption = 'Не совсем старшая школа, но по-моему хорошее'
        elif 'last_selfie' in filename:
            caption = 'Последнее селфи'
        await bot.send_photo(
            callback_query.from_user.id,
            photo=file_id,
            caption=caption
        )


@dp.message_handler(commands=['about'])
async def process_command_about(message: types.Message):
    """Sends small text post."""
    await bot.send_message(
        message.from_user.id,
        text=text(*ABOUT_POST, sep=' ')
    )


@dp.message_handler(commands=['repo'])
async def process_command_repo(message: types.Message):
    """Sends a message with url to repo with source code of this bot."""
    await bot.send_message(
        message.from_user.id,
        text=text(
            bold('Ссылка на репозиторий:'),
            code(REPO_URL),
            sep='\n',
        ), parse_mode=ParseMode.MARKDOWN_V2
    )


@dp.message_handler(
    content_types=types.ContentType.VOICE
)
async def voice_message_handler(message: types.Message):
    """
    Handler for voice messages. Chooses which command
    to start depending on keywords contained by voice message.
    """
    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
    else:
        await message.reply('Формат данных не поддерживается.')

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = BOT_DIR / 'tmp' / file_id
    await bot.download_file(file_path, file_on_disk)
    await message.reply('Голосовое сообщение получено.')
    translated_text = voice_to_text(file_on_disk)

    for f in os.listdir(BOT_DIR / 'tmp'):
        if file_id in f:
            os.remove(BOT_DIR / 'tmp' / f)

    await bot.send_message(
        message.from_user.id,
        text=translated_text
    )




@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    """Last resort if any other handlers didn't catch anything."""
    message_text = text('Я не знаю, что с этим делать.',
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)




if __name__ == '__main__':
    executor.start_polling(dp)
