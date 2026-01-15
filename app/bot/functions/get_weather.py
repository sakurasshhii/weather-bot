import openmeteo_requests
import logging
import pandas as pd

from aiogram.types import Message
from app.bot.lexic.coordinates import coordinates


logger = logging.getLogger(__name__)
__all__ = ['get_weather_api', 'get_current']



params_duration: dict[str, dict[str, list[str] | str]] = {
    "current": {
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ],
    },
    "today": {
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "wind_direction_10m"
            "weather_code"
        ],
        "start_hour": "",
        "end_hour": ""
    },
    "week": {
        "daily": [
            "temperature_2m_max",
            "temperature_2m_mean",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant"
            "weather_code"
        ],

    }
}


async def get_params(latitude: float, longitude: float, duration: str = 'current'):
    ''' 
    Генератор параметров для API-запроса погоды, 
    в зависимости от выбранного промежутка времени
    '''
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto"
    }
    params.update(params_duration[duration])

    return params

async def get_weather_api(message: Message, city: str = 'Мурманск', duration: str = 'current'):
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

    url = "https://api.open-meteo.com/v1/forecast"
    params = await get_params(latitude, longitude, duration)
    responses = await openmeteo.weather_api(url, params=params)

    # Process first location
    response = responses[0]
    logger.info(
        f'Weather request from chat {message.chat.id}:\n' \
        f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n" \
        f"Elevation: {response.Elevation()} m asl\n" \
        f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s"
    )

    return response

async def get_current(response) -> pd.Series:
    '''
    Получение текущей погоды из результата запроса
    '''
    current = response.Current()
    variables = [current.Variables(i).Value() for i in range(4)]

    data = pd.Series(
        variables, 
        ['current_temperature_2m', 'current_relative_humidity_2m', 'current_precipitaion', 'current_wind_speed_10m']
    )

    return data

async def response_maker(response):
    pass
