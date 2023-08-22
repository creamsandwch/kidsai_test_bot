import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram.utils.markdown import bold, code, italic, text
from config import TOKEN, URL, MEDIA_PATH
from keyboards import voices_inline_kb
from utils import search_for_file_by_name

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
    await message.reply(
        'Привет!\nИспользуй /help, чтобы узнать список доступных команд',
    )


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(
        bold('Команды:'),
        '/photos - мои фото',
        '/voices - мои голосовые с короткими рассказами',
        '/about - про моё главное увлечение',
        '/repo - ссылка на репозиторий с исходниками этого бота',
        sep='\n'
    )
    await message.reply(
        text=msg, parse_mode=ParseMode.MARKDOWN
    )


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
async def process_callback_lovestory_button(
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


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    """Last resort if any other handlers didn't catch anything."""
    message_text = text('Я не знаю, что с этим делать.',
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
