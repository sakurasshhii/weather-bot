from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from app.bot.lexic.coordinates import coordinates, city_names
from app.bot.keyboards.weather import location_kboard, geo_kboard, duration_kboard
from app.bot.lexic.lexic import WEATHER_RU
# from app.bot.filters import IsValidCity
from app.bot.weather_processor import Weather, Duration
import app.infrastructure.user_data as users

import logging


logger = logging.getLogger(__name__)

api_router = Router()
weather_router = Router()


# [кнопка dur] Передача конечного запроса погоды
@weather_router.callback_query(F.data.in_(['current', 'today', 'week']))
async def weather_with_duration(cback: CallbackQuery):
    if cback.message:
        await cback.message.answer(
            text=WEATHER_RU['weather_ask']
        )
        user = await users.get_user(str(cback.from_user.id))
        weather = Weather(
            latitude=user["coordinates"]["latitude"],
            longitude=user["coordinates"]["longitude"]
        )
        duration = Duration[cback.data.upper()]
        result = await weather.get_weather(duration=duration)
        await cback.message.answer(
            text=result
        )
    else:
        logger.warning('CallbackQuery object has no message.answer')


# Уточнение запроса погоды: сейчас, сегодня, на нделю
@weather_router.message(Command(commands='duration'))
async def process_ask_duration(message: Message):
    await message.answer(
        text=WEATHER_RU['pick_dur'],
        reply_markup=duration_kboard
    )


# [кнопка геолокация] Ответ на геолокацию: сохранение в бд
@weather_router.message(F.location)
async def process_got_location(message: Message):
    if message.from_user and message.location:
        await users.add_user(
            user_id=str(message.from_user.id),
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
        await message.answer(
            text=WEATHER_RU['got_loc'],
            reply_markup=ReplyKeyboardRemove()
        )

        await process_ask_duration(message)


# Ответ на название города: сохранение в бд
@weather_router.message(F.text.lower().in_(city_names))
async def process_got_city(message: Message):
    if message.text and message.from_user:
        city = message.text.capitalize()
        lat = coordinates[city]["latitude"]
        lon = coordinates[city]["longitude"]
        
        await users.update_user_info(
            user_id=str(message.from_user.id),
            coordinates=(lat, lon),
            city=city
        )

        await process_ask_duration(message)


# [кнопка ввести локацию] Запрос: введите ваш город
@weather_router.callback_query(F.data == 'ask_city')
async def process_ask_city(cback: CallbackQuery):
    if cback.message:
        await cback.message.answer(
            text=WEATHER_RU['other_loc'],
            reply_markup=ReplyKeyboardRemove()
        )


# [кнопка определить локацию] Запрос: отправьте геопозицию
@weather_router.callback_query(F.data == 'ask_location')
async def process_ask_loc(cback: CallbackQuery):
    if cback.message:
        await cback.message.answer(
            text=WEATHER_RU['req_loc_btn'],
            reply_markup=geo_kboard  # добавить в клавиатуру возможность вернуться назад
        )


# Сменить или задать локацию
@weather_router.message(Command(commands='set_location'))
async def process_set_location(message: Message):
    await message.answer(
        text=WEATHER_RU['req_loc_txt'],
        reply_markup=location_kboard
    )

# Запуск запроса погоды
@weather_router.message(Command(commands='start_weather'))
async def process_weather_main(message: Message):
    if message.from_user:
        user = await users.get_user(str(message.from_user.id))
        if user["coordinates"]:
            await process_ask_duration(message)
        else:
            await process_set_location(message)
    else:
        logger.warning('message has no data from user')
