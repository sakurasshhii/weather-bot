from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.bot.lexic import WEATHER_RU, WEATHER_DURATION


# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()

# Кнопки запроса локации
geo_btn = KeyboardButton(text=WEATHER_RU['req_loc_btn'], request_location=True)
input_geo_btn = KeyboardButton(text=WEATHER_RU['other_loc_btn'])

# Добавляем кнопки в билдер
kb_builder.row(geo_btn, input_geo_btn)

# Клавиатура запроса локации
req_location_keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True
    )

# Кнопки для клавиатуры погоды: сейчас, сегодня, на неделю
duration_btn = [
    InlineKeyboardButton(text=txt, callback_data=key)
    for key, txt in WEATHER_DURATION.items()
]

duration_kboard = InlineKeyboardMarkup(
    inline_keyboard=[duration_btn]
)