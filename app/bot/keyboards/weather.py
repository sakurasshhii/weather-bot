from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    reply_keyboard_remove
)
from app.bot.lexic import WEATHER_RU


geo_btn = KeyboardButton(text=WEATHER_RU['req_location_but'], request_location=True)

req_location_keyboard = ReplyKeyboardMarkup(keyboard=[[geo_btn]])
