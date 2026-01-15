import openmeteo_requests
import logging
import pandas as pd

from aiogram.types import Message
from app.bot.lexic.coordinates import coordinates


logger = logging.getLogger(__name__)
__all__ = ['get_weather_api']


# Набор параметров для API-запроса: сейчас, на день, на неделю
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
            "wind_direction_10m",
            "weather_code"
        ],
        "start_hour": "2026-01-15T10:00",
        "end_hour": "2026-01-15T20:00"
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
        "start_date": "2026-01-15",
        "end_date": "2026-01-22"
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


async def weather_cur_resp(response_cur) -> pd.Series:
    '''
    Обрабатывает ответ на запрос погоды сейчас
    '''
    names = params_duration["current"]["current"]
    variables = [response_cur.Variables(i).Value() for i in range(len(names))]

    current_series_pd = pd.Series(names, variables)

    return current_series_pd


async def weather_dur_resp(response_dur, duration, key) -> pd.DataFrame:
    '''
    Обрабатывает ответ на запрос погоды сегодня / на неделю
    
    :param response_dur: class 'openmeteo_sdk.VariablesWithTime.VariablesWithTime'
    :param duration: клиентская кнопка 'today' / 'week'
    :param key: соответствующий серверный параметр 'hourly' / 'daily'
    :return: таблица погодных показателей за запрашиваемый период
    :rtype: DataFrame
    '''
    time_mark = pd.date_range(
        start = pd.to_datetime(response_dur.Time(), unit='s'),
        end = pd.to_datetime(response_dur.TimeEnd(), unit='s'),
        freq = pd.Timedelta(seconds=response_dur.Interval()),
        inclusive='left'
    )

    variable_names = params_duration[duration][key]
    time_data = {
        variable_names[i]:
        response_dur.Variables(i).ValuesAsNumpy()
        for i in range(response_dur.VariablesLength())
    }

    dur_dataframe_pd = pd.DataFrame(data=time_data)
    dur_dataframe_pd.index = time_mark

    return dur_dataframe_pd


async def get_weather_api(message: Message, city: str = 'Мурманск', duration: str = 'current'):
    '''
    Функция API запроса погоды с сервера
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

    # Answer recieved
    response = responses[0]
    logger.info(
        f'Weather request from chat {message.chat.id}:\n' \
        f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n" \
        f"Elevation: {response.Elevation()} m asl\n" \
        f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s"
    )

    match duration:
        case 'current':
            result_pd = await weather_cur_resp(response.Current())
            return result_pd
        case 'today':
            result_pd = await weather_dur_resp(response.Hourly(), duration, 'hourly')
            return result_pd
        case 'week':
            result_pd = await weather_dur_resp(response.Daily(), duration, 'daily')
            return result_pd
