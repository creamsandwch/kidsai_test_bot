from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_lovestory = InlineKeyboardButton(
    'История первой любви',
    callback_data='love_story'
)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
inline_kb.add(button_lovestory)
