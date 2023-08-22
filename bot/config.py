import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

MEDIA_PATH = Path(__file__).resolve().parent.parent / 'database' / 'media'

URL = 'http://127.0.0.1:8000/api/v1/media_ids/'

MY_ID = os.getenv('MY_ID')
