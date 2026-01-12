from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

import app.bot.functions as func
# import pandas as pd


router = Router()

@router.message(Command(commands=['weather']))
async def process_weather(message: Message):
    # response = func.get_weather(city='Москва')
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
    # # Process hourly data. The order of variables needs to be the same as requested.
    # hourly = response.Hourly()
    # hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    # hourly_data = {"date": pd.date_range(
    #     start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    #     end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
    #     freq = pd.Timedelta(seconds = hourly.Interval()),
    #     inclusive = "left"
    # )}

    # hourly_data["temperature_2m"] = hourly_temperature_2m

    # hourly_dataframe = pd.DataFrame(data = hourly_data)
    # print("\nHourly data\n", hourly_dataframe)
    await message.answer('weather')
