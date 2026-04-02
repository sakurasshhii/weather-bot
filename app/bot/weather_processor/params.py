'''
Хранит класс Params, Duration.
Отвечает за конструирование параметров запроса погоды.
'''
import datetime as dt
import json
import logging

from enum import Enum, auto


logger = logging.getLogger(__name__)


class Duration(Enum):
    '''Параметр временных рамок для запроса погоды'''
    CURRENT = auto()
    TODAY = auto()
    WEEK = auto()
    
    def display_as_key(self) -> str:
        '''Возвращает ключ-серверный параметр'''
        names = {
            Duration.CURRENT: 'current',
            Duration.TODAY: 'hourly',
            Duration.WEEK: 'daily'
        }
        return names[self]


class ParamsMeta(type):
    '''Единичная загрузка шаблона для работы с параметрами'''
    _params_temp = None

    def __new__(cls, name, bases, namespace):
        if cls._params_temp is None:
            logger.debug(f'[{cls.__name__}] preparing params_temp: reading from json file...')
            with open(r"app\bot\weather_processor\data\params_duration.json", encoding="utf-8", mode="r") as f:
                cls._params_temp = json.load(f)
        namespace['_params_temp'] = cls._params_temp
        
        return super().__new__(cls, name, bases, namespace)


class Params(metaclass=ParamsMeta):
    '''Подготовка параметров для API-запроса'''
    UTC_OFFSET = dt.timezone(dt.timedelta(hours=3))

    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude
        # Добавить кэширование
    
    async def prepare_params(self, duration: Duration):
        ''' 
        Подготовка параметров для API-запроса погоды,
        в зависимости от выбранного промежутка времени
        '''
        params = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "timezone": "auto"
        }
        params.update(self._params_temp[duration.name]) # type: ignore — атрибут добавлен через метакласс
        match duration.name:
            case "TODAY":
                hour_st, hour_en = await self.__class__.calculate_day()
                params.update({
                    "start_hour": hour_st,
                    "end_hour": hour_en
                })
            case "WEEK":
                date_st, date_en = await self.__class__.calculate_week()
                params.update({
                    "start_date": date_st,
                    "end_date": date_en
                })

        return params
    
    @classmethod
    async def calculate_day(cls):
        '''Рассчитывает временные рамки на день'''
        now_hour_dt = dt.datetime.now(tz=cls.UTC_OFFSET)
        end_hour_dt = now_hour_dt.replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)
        logger.info(f"time spread for one day: {now_hour_dt.isoformat()} to {end_hour_dt.isoformat()}")
        
        return now_hour_dt.strftime(r'%Y-%m-%dT%H:00'), end_hour_dt.strftime(r'%Y-%m-%dT%H:00')

    @classmethod
    async def calculate_week(cls):
        '''Рассчитывает временные рамки на неделю'''
        now_dt = dt.date.today()
        end_dt = now_dt + dt.timedelta(days=7)
        logger.info(f"time spread for one week: {now_dt.isoformat()} to {end_dt.isoformat()}")
        
        return now_dt.isoformat(), end_dt.isoformat()

