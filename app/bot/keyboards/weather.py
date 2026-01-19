from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.bot.lexic import WEATHER_RU, WEATHER_DURATION_BTN, WEATHER_LOC_BTN


# # Инициализируем билдер
# kb_builder = ReplyKeyboardBuilder()

# Кнопки запроса локации

# input_geo_btn = KeyboardButton(text=WEATHER_RU['other_loc_btn'])

# # Добавляем кнопки в билдер
# kb_builder.row(geo_btn, input_geo_btn)

# # Клавиатура запроса локации
# req_location_keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
#     resize_keyboard=True
#     )


# Кнопки запроса локации: ввести вручную, отправить координаты
loc_btn = [
    InlineKeyboardButton(text=txt, callback_data=key)
    for key, txt in WEATHER_LOC_BTN.items()
]

location_kboard = InlineKeyboardMarkup(
    inline_keyboard=[loc_btn]
)

# Кнопка отправить геолокацию
geo_btn = KeyboardButton(text=WEATHER_RU['req_loc_btn'], request_location=True)
geo_kboard = ReplyKeyboardMarkup(
    keyboard=[[geo_btn]],
    resize_keyboard=True
)

# Кнопки для клавиатуры погоды: сейчас, сегодня, на неделю
duration_btn = [
    InlineKeyboardButton(text=txt, callback_data=key)
    for key, txt in WEATHER_DURATION_BTN.items()
]

duration_kboard = InlineKeyboardMarkup(
    inline_keyboard=[duration_btn]
)