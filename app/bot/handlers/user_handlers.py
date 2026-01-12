from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

import pandas as pd
import openmeteo_requests

from app.bot.lexic import coordinates


api_router = Router()

@api_router.message(Command(commands=['weather']))
async def process_weather(message: Message):

    city = 'Москва'
    openmeteo = openmeteo_requests.AsyncClient()

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coordinates[city]["latitude"],
        "longitude": coordinates[city]["longitude"],
        "current": ["temperature_2m", "relative_humidity_2m"],
        "timezone": "auto"
    }
    responses = await openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    current = response.Current()
    current_temperature_2m = current.Variables(0).Value() # pyright: ignore[reportOptionalMemberAccess]
    current_relative_humidity_2m = current.Variables(1).Value() # pyright: ignore[reportOptionalMemberAccess]

    await message.answer(
        f'Current temperature: {round(current_temperature_2m, 2)}\n'\
        f'Current relative humidity: {current_relative_humidity_2m}'
    )
