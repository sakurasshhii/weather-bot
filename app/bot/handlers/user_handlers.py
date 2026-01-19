from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from app.bot.lexic.coordinates import *
from app.bot.keyboards.weather import location_kboard, geo_kboard
from app.bot.lexic.lexic import WEATHER_RU
from app.bot.lexic.coordinates import coordinates
from app.bot.filters import IsValidCity
import app.bot.functions as bot_func
import app.infrastructure.user_data as users

import logging
import pandas as pd


logger = logging.getLogger(__name__)

api_router = Router()
weather_router = Router()


@api_router.message(Command(commands=['weather']))
async def process_weather(message: Message, city: str | None = None, duration: str = 'current'):
    '''
    Главный погодный хэндлер: обрабатывает все запросы на погоду.
    
    :param message: tg update
    :type message: Message
    :param city: Город
    :param duration: Запрос на погоду сейчас / сегодня / недельный
    '''
    if city is not None or message.location is None:
        result = await bot_func.get_weather_api(user_loc=city, duration=duration)
    else:
        result = await bot_func.get_weather_api(user_loc=message.location, duration=duration)
    
    await message.answer(
        text=repr(result),
        reply_markup=ReplyKeyboardRemove()
    )
    '''
    разбить на разные команды:
    /weather_now
    /weather_today
    /weather_week
    '''

# [кнопка геолокация] Ответ на геолокацию: сохранение в бд
@weather_router.message(F.location)
async def process_got_location(message: Message):
    if message.from_user and message.location:
        await users.add_user(
            user_id=message.from_user.id,
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
        await message.answer(
            text='-data added-',
            reply_markup=ReplyKeyboardRemove()
        )
    # await process_weather(message)


# Ответ на название города: сохранение в бд
@weather_router.message(F.text.lower().in_(city_names))
async def process_got_city(message: Message):
    if message.text and message.from_user:
        city = message.text.capitalize()
        lat = coordinates[city]["latitude"]
        lon = coordinates[city]["longitude"]
        
        await users.update_user_info(
            user_id=message.from_user.id,
            coordinates=(lat, lon),
            city=city
        )

    # await process_weather(message, message.text)
    # также вспомогательная ф-я с сохранением в бд


# [кнопка ввести локацию] Запрос: введите ваш город
@weather_router.callback_query(F.data == 'ask_city')
async def process_ask_city(cback: CallbackQuery):
    if cback.message:
        await cback.message.answer(WEATHER_RU['other_loc'])


# [кнопка определить локацию] Запрос: отправьте геопозицию
@weather_router.callback_query(F.data == 'ask_location')
async def process_ask_loc(cback: CallbackQuery):
    if cback.message:
        await cback.message.answer(
            text='-press button-',
            reply_markup=geo_kboard  # добавить в клавиатуру возможность вернуться назад
        )


# Запуск запроса погоды
@weather_router.message(Command(commands='start_weather'))
async def process_weather_main(message: Message):
    data = await users.load_data()
    if data[str(message.from_user.id)]["coordinates"]: # type: ignore
        pass
    else:
        await message.answer(
        text=WEATHER_RU['req_loc_txt'],
        reply_markup=location_kboard
    )
    await message.answer('Конец выполнения функции process_weather_main')


@weather_router.message(Command(commands='duration'))
async def process_ask_duration(message: Message):
    await message.answer(
        text=''
    )
