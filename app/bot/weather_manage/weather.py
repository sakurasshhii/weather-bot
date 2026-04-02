import openmeteo_requests
import logging
import pandas as pd
from abc import ABC, abstractmethod

from app.bot.weather_manage.params_constructor import Params


logger = logging.getLogger(__name__)


class Weather(ABC):
    _openmeteo = openmeteo_requests.AsyncClient()
    _url = "https://api.open-meteo.com/v1/forecast"

    async def __init__(self, latitude, longitude, when='current'):
        self.latitude = latitude
        self.longitude = longitude
        params_maker = Params(
            latitude=self.latitude,
            longitude=self.longitude
        )
        self._params = await params_maker.get_params(when)
        # добавить обновление класса при смене координат

    @abstractmethod
    async def make_pd(self, response):
        'Обрабатывает ответ и возвращает таблицу'

    @abstractmethod
    async def format_pd(self):
        'Обрабатывает таблицу и возвращает читаемый ответ погоды'

    async def get_weather(self):
        'Запрос погоды по параметрам'
        responses = await self._openmeteo.weather_api(self._url, params=self._params)
        response = responses[0]  # ответ сервера
        
        return response
    
class CurrentWeather(Weather):
    async def __init__(self, latitude, longitude):
        await super().__init__(latitude, longitude, when='current')

    async def make_pd(self, response) -> pd.Series:
        'Обрабатывает ответ на запрос погоды сейчас'
        names = self._params["current"]
        variables = [response.Variables(i).Value() for i in range(len(names))]

        current_series_pd = pd.Series(variables, names)

        logger.info(f'{self.__class__.__name__} — weather data processed:\n\n{current_series_pd}')

        return current_series_pd
    
    async def format_pd(self, data):
        return await super().format_pd()

    async def get_weather(self):
        response = await super().get_weather()
        result_pd = self.make_pd(response.Current)
        return await self.format_pd(result_pd)

