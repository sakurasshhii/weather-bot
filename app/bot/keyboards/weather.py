from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    reply_keyboard_remove
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.bot.lexic import WEATHER_RU


# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Создаем кнопки для клавиатуры
geo_btn = KeyboardButton(text=WEATHER_RU['req_loc_btn'], request_location=True)
input_geo_btn = KeyboardButton(text=WEATHER_RU['other_loc_btn'])

# Добавляем кнопки в билдер
kb_builder.row(geo_btn, input_geo_btn)

# Клавиатура для запроса локации
req_location_keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True
    )
