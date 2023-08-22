import asyncio
import logging
import os
from pathlib import Path

import aiohttp
from aiogram import Bot
from dotenv import load_dotenv

logging.basicConfig(
    format=(
        '%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s'
        ' [%(asctime)s]  %(message)s'
    ),
    level=logging.DEBUG
)

load_dotenv()
MY_ID = os.getenv('MY_ID')
bot = Bot(token=os.getenv('BOT_TOKEN'))

MEDIA_PATH = Path(__file__).resolve().parent.parent / 'database' / 'media'

URL = 'http://127.0.0.1:8000/api/v1/media_ids/'


async def send_post_media_id(data, url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data) as response:
            return response.status


async def store_ids_for_my_files(folder, method, file_attr):
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
                await send_post_media_id(data, URL)
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
        store_ids_for_my_files('photos', bot.send_photo, 'photo')
    ),
    loop.create_task(
        store_ids_for_my_files('voice', bot.send_video, 'voice')
    ),
    loop.create_task(
        store_ids_for_my_files('audio', bot.send_audio, 'audio')
    )
]

waited_tasks = asyncio.wait(tasks)
loop.run_until_complete(waited_tasks)
loop.close()
