from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from app.bot.lexic.coordinates import *
from app.bot.keyboards.weather import *
from app.bot.lexic.lexic import WEATHER_RU
from app.bot.functions import get_weather_api

import openmeteo_requests
import logging
import pandas as pd


logger = logging.getLogger(__name__)

api_router = Router()
weather_router = Router()


# Запрос локации для погоды
@weather_router.message(Command(commands=['weather_in_location']))
async def process_ask_location(message: Message):
    await message.answer(
        text=WEATHER_RU['req_loc_txt'],
        reply_markup=req_location_keyboard
    )


@api_router.message(Command(commands=['weather']))
async def process_weather(message: Message, city='Мурманск'):
    response = await get_weather_api(message=message, city=city)

    current = response.Current()

    variables = []
    for i in range(4):
        variables.append(current.Variables(i).Value()) # pyright: ignore[reportOptionalMemberAccess]
    # current_temperature_2m = current.Variables(0).Value()  # pyright: ignore[reportOptionalMemberAccess]
    # current_relative_humidity_2m = current.Variables(1).Value()  # pyright: ignore[reportOptionalMemberAccess]
    # current_precipitaion = current.Variables(2).Value() # pyright: ignore[reportOptionalMemberAccess]
    # current_wind_speed_10m = current.Variables(3).Value() # pyright: ignore[reportOptionalMemberAccess]

    data = pd.Series(
        variables, 
        ['current_temperature_2m', 'current_relative_humidity_2m', 'current_precipitaion', 'current_wind_speed_10m']
    )
    # data = await get_weather_api(message=message, city=city)

    await message.answer(
        f'Current temperature: {round(data['current_temperature_2m'], 1)}\n' \
        f'Relative humidity: {round(data['current_relative_humidity_2m'], 1)}\n' \
        f'Precipitaion: {round(data['current_precipitaion'])}\n' \
        f'Wind speed: {round(data['current_wind_speed_10m'], 1)}',
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на геолокацию: отправка погоды.
@weather_router.message(F.location)
async def process_weather_loc(message: Message):
    await process_weather(message)


# Запрос: введите ваш город
@weather_router.message(F.text == WEATHER_RU['other_loc_btn'])
async def process_other_location(message: Message):
    await message.answer(WEATHER_RU['other_loc'])


# Ответ на название города: отправка погоды.
@weather_router.message(F.text.lower().in_(city_names))
async def process_weather_other(message: Message):
    print(message.model_dump_json())
    await process_weather(message, message.text)
