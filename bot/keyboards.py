from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_lovestory = InlineKeyboardButton(
    'Первая любовь',
    callback_data='voicebtn_love_story'
)
button_sql_vs_nosql = InlineKeyboardButton(
    'SQL и NoSQL',
    callback_data='voicebtn_sql_vs_nosql'
)
button_chatgpt_for_grandma = InlineKeyboardButton(
    'ChatGPT для бабушки',
    callback_data='voicebtn_chatgpt'
)

inline_kb = InlineKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=1
)
inline_kb.add(
    button_lovestory,
    button_chatgpt_for_grandma,
    button_sql_vs_nosql
)
