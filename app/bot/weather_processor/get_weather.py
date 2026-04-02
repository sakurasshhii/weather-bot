import logging
import openmeteo_requests
import pandas as pd

from .custom_exceptions import WeatherException
from .formatter import Formatter
from .params import Duration, Params


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Weather:
    '''
    Класс API-запросов погоды с сервера.
    Хранит в себе координаты и выдает ответ, в зависимости от настроек (duration)    
    '''
    
    URL = "https://api.open-meteo.com/v1/forecast"
    OPENMETEO = openmeteo_requests.AsyncClient()
    MAX_CACHE = 3
    formatter = Formatter()

    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude
        self._params = Params(latitude=latitude, longitude=longitude)
        self._cache = {}
        self._keys = []
    
    async def get_weather(self, duration: Duration):
        params = await self._params.prepare_params(duration)

        # key = hash(params)
        # if key in self._cache:
        #     return self._cache[key]
        
        logger.info(f'prepared params: {params}')
        responses = await self.__class__.OPENMETEO.weather_api(
            url=self.__class__.URL,
            params=params
        )
        response = responses[0]
        logger.info(f"response recieved...\n" \
            f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E\n" \
            f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s"
        )

        await self.formatter.initialize()
        match duration.name:
            case 'CURRENT':
                result_pd = await self.__class__.prepare_response_curr(response.Current(), duration)
                return await self.formatter.from_series(result_pd)
            case 'TODAY':
                result_pd = await self.__class__.prepare_response_day(response.Hourly(), duration)
                return await self.formatter.from_dataframe(result_pd, mode=duration)
            case 'WEEK':
                result_pd = await self.__class__.prepare_response_day(response.Daily(), duration)
                return await self.formatter.from_dataframe(result_pd, mode=duration)
            case _:
                raise WeatherException(name=__name__, txt=f'Неверно задана длительность Duration: {duration}')
    
    # async def cache_check(self, params):
    #     key = hash(params)
    #     if key in self._cache:
    #         return self._cache[key]
    #     if len(self._cache) >= self.__class__.MAX_CACHE:
    #         pass
        ############################# to do ###########################

    @staticmethod
    async def prepare_response_curr(response, duration: Duration) -> pd.Series:
        '''Оформляет в таблицу ответ на запрос погоды сейчас'''
        names = Params._params_temp[duration.name][duration.display_as_key()] # type: ignore
        variables = [response.Variables(i).Value() for i in range(len(names))]

        current_series_pd = pd.Series(variables, names)

        # logger.info(f'weather data processed:\n\n{current_series_pd}')

        return current_series_pd

    @staticmethod
    async def prepare_response_day(response, duration: Duration) -> pd.DataFrame:
        '''Оформляет в таблицу ответ на запрос погоды today/ week'''
        time_mark = pd.date_range(
            start = pd.to_datetime(response.Time(), unit='s'),
            end = pd.to_datetime(response.TimeEnd(), unit='s'),
            freq = pd.Timedelta(seconds=response.Interval()),
            inclusive='right'
        )

        variable_names = Params._params_temp[duration.name][duration.display_as_key()] # type: ignore
        time_data = {
            variable_names[i]:
            response.Variables(i).ValuesAsNumpy()
            for i in range(response.VariablesLength())
        }

        dur_dataframe_pd = pd.DataFrame(data=time_data)
        dur_dataframe_pd.index = time_mark

        return dur_dataframe_pd
