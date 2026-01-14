import openmeteo_requests
import logging
import pandas as pd

from aiogram.types import Message
from app.bot.lexic.coordinates import coordinates


logger = logging.getLogger(__name__)


async def get_weather_api(message: Message, city='Мурманск'):
    '''
    Функция API запроса погоды
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
    logger.info(
        f'Weather request from chat {message.chat.id}:\n' \
        f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n" \
        f"Elevation: {response.Elevation()} m asl\n" \
        f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s"
    )

    current = response.Current()

    variables = []
    for i in range(4):
        variables.append(current.Variables(i).Value()) # pyright: ignore[reportOptionalMemberAccess]
    # current_temperature_2m = current.Variables(0).Value()  # pyright: ignore[reportOptionalMemberAccess]
    # current_relative_humidity_2m = current.Variables(1).Value()  # pyright: ignore[reportOptionalMemberAccess]
    # current_precipitaion = current.Variables(2).Value() # pyright: ignore[reportOptionalMemberAccess]
    # current_wind_speed_10m = current.Variables(3).Value() # pyright: ignore[reportOptionalMemberAccess]

    result = pd.Series(
        variables, 
        ['current_temperature_2m', 'current_relative_humidity_2m', 'current_precipitaion', 'current_wind_speed_10m']
    )

    return result
