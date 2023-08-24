## kidsai test bot

### Telegram bot done with:
    - aiogram
    - django + DRF (for storing file_ids)
    - speech_recognition (Google API)
### Provides some basic commands:
    - /voice - to play my recorded stories
    - /photo - my last selfie and highshool photo
    - /about - small post about my passion
    - /repo - contains an url to this repo
Uses speech recognition to search through recognized text and find some keywords, which are connected to commands, and sends users message with command based on received voice message.

### Launch:
You should make your .env file and fill out these vars:
```
BOT_TOKEN=<your bot token>
MY_ID=<bot admin chat id>
DJANGO_SECRET_KEY=<your django secret key>
```
In base dir, you should start a venv  and then install all of dependencies (or just plainly install them):
```
pip install -r requirements.txt
```
Then you should set up the database:
```
cd database/
python manage.py makemigrations
python manage.py migrate
```
Upload media files that are already stored in database/media/
(this script should be launched once for every new file is added to media/ to create db instance with telegram file_id for new file):
```
cd ../bot
python upload_my_files.py
```
And then just launch django localserver and bot polling in separate terminals:
```
# in database/ dir:
python manage.py runserver
# in bot/ dir:
python bot.py
```
