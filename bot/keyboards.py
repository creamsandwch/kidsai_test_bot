from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

button_hi = KeyboardButton('Привет!')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)