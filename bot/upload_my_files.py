import asyncio
import logging
import os

from aiogram import Bot
from dotenv import load_dotenv

from config import MEDIA_PATH, MY_ID, URL
from utils import (
    create_media_id,
    update_media_id,
    search_for_file_by_name
)

logging.basicConfig(
    format=(
        '%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s'
        ' [%(asctime)s]  %(message)s'
    ),
    level=logging.DEBUG
)

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))


async def store_ids_for_my_files(folder, method, file_attr):
    """
    Telegram gives media files unique ids
    in order to optimise its sending.
    If filename exists in db, updates its telegram id.
    """
    folder_path = MEDIA_PATH / folder
    logging.info(msg=f'current folder is {folder_path}')
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(MY_ID, file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id

            try:
                data = {'file_id': file_id, 'filename': filename}
                obj_list = await search_for_file_by_name(
                    url=URL, filename=filename
                )
                if len(obj_list) == 1:
                    id = obj_list[0]
                    logging.info(
                        'Updating telegram id on file with db_id = {}'.format(id)
                    )
                    await update_media_id(
                        data=data, url=URL, id=obj_list[0]['id']
                    )
                else:
                    await create_media_id(data=data, url=URL)
            except Exception as exc:
                logging.error(
                    'File {} id was not saved: {}'.format(filename, exc)
                )
            else:
                logging.info(
                    (
                        'File {} with id {}'.format(filename, file_id),
                        ' successfully saved to database'
                    )
                )

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(
        store_ids_for_my_files('photo', bot.send_photo, 'photo')
    ),
    loop.create_task(
        store_ids_for_my_files('voice', bot.send_voice, 'voice')
    ),
    loop.create_task(
        store_ids_for_my_files('audio', bot.send_audio, 'audio')
    )
]

waited_tasks = asyncio.wait(tasks)
loop.run_until_complete(waited_tasks)
loop.close()
