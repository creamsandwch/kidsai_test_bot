from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# voice messages keyboard (on command /voices)
button_lovestory = InlineKeyboardButton(
    'Первая любовь',
    callback_data='voicebtn_love_story'
)
button_sql_vs_nosql = InlineKeyboardButton(
    'SQL и NoSQL',
    callback_data='voicebtn_sql_vs_nosql'
)
button_chatgpt_for_grandma = InlineKeyboardButton(
    'GPT для бабушки',
    callback_data='voicebtn_chatgpt'
)
voices_inline_kb = InlineKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=1
)
voices_inline_kb.add(
    button_lovestory,
    button_chatgpt_for_grandma,
    button_sql_vs_nosql
)

# photo messages keyboard (on command /photos)
button_last_selfie = InlineKeyboardButton(
    'Последнее селфи',
    callback_data='photobtn_last_selfie',
)
button_highschool_photo = InlineKeyboardButton(
    'Фото из старшей школы',
    callback_data='photobtn_highschool_photo'
)
photos_inline_kb = InlineKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=1
)
photos_inline_kb.add(
    button_last_selfie,
    button_highschool_photo
)
