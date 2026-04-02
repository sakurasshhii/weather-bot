import openmeteo_requests
import logging
import pandas as pd

from .weather_param import get_params, params_duration
from .formatter import *


logger = logging.getLogger(__name__)
__all__ = ['get_weather_api']


async def weather_cur_resp(response_cur) -> pd.Series:
    '''
    Обрабатывает ответ на запрос погоды сейчас
    '''
    names = params_duration["current"]["current"]
    variables = [response_cur.Variables(i).Value() for i in range(len(names))]

    current_series_pd = pd.Series(variables, names)

    logger.info(f'weather data processed:\n\n{current_series_pd}')

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
        inclusive='right'
    )

    variable_names = params_duration[duration][key]
    time_data = {
        variable_names[i]:
        response_dur.Variables(i).ValuesAsNumpy()
        for i in range(response_dur.VariablesLength())
    }

    dur_dataframe_pd = pd.DataFrame(data=time_data)
    dur_dataframe_pd.index = time_mark

    logger.info(f'weather data processed:\n\n{dur_dataframe_pd}')

    return dur_dataframe_pd


async def get_weather_api(latitude, longitude, duration) -> str:
    '''
    Функция API запроса погоды с сервера.
    
    return: таблица данных о погоде
    rtype: pd Series/ DataFrame, в зависимости от duration
    '''
    openmeteo = openmeteo_requests.AsyncClient()

    url = "https://api.open-meteo.com/v1/forecast"

    params = await get_params(latitude, longitude, duration)
    responses = await openmeteo.weather_api(url, params=params)

    # Answer recieved
    response = responses[0]
    logger.info(
        f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n" \
        f"Elevation: {response.Elevation()} m asl\n" \
        f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s"
    )

    match duration:
        case 'current':
            result_pd = await weather_cur_resp(response.Current())
            return await str_format_current(result_pd)
        case 'today':
            result_pd = await weather_dur_resp(response.Hourly(), duration, 'hourly')
            return await str_format_today(result_pd)
        case 'week':
            result_pd = await weather_dur_resp(response.Daily(), duration, 'daily')
            return await str_format_week(result_pd)
    
    return "Error during get_weather_api"
