from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from app.bot.lexic.coordinates import *
from app.bot.keyboards.weather import *
from app.bot.lexic.lexic import WEATHER_RU

import openmeteo_requests


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
    '''
    Отправка погоды пользователю через open-meteo API.
    Основной погодный хендлер.
    '''
    if not message.location:
        latitude = coordinates[city.capitalize()]["latitude"]
        longitude = coordinates[city.capitalize()]["longitude"]
    else:
        latitude = message.location.latitude
        longitude = message.location.longitude

    openmeteo = openmeteo_requests.AsyncClient()

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "timezone": "auto"
    }
    responses = await openmeteo.weather_api(url, params=params)

    # Process first location
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()  # pyright: ignore[reportOptionalMemberAccess]
    current_relative_humidity_2m = current.Variables(1).Value()  # pyright: ignore[reportOptionalMemberAccess]
    current_precipitaion = current.Variables(2).Value() # pyright: ignore[reportOptionalMemberAccess]
    current_wind_speed_10m = current.Variables(3).Value() # pyright: ignore[reportOptionalMemberAccess]

    await message.answer(
        f'Current temperature: {round(current_temperature_2m, 1)}\n' \
        f'Relative humidity: {round(current_relative_humidity_2m, 1)}\n' \
        f'Precipitaion: {current_precipitaion}\n' \
        f'Wind speed: {round(current_wind_speed_10m, 1)}',
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
