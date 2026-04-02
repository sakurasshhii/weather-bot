'''
Хранит класс Formatter
'''
import json
import logging
import pandas as pd

from .params import Duration
from .data.format_temp import temp_today_mean, temp_week


logger = logging.getLogger(__name__)


class Formatter:
    '''Форматирует табличные данные для вывода ответа пользователю'''
    __initialized = False

    @classmethod
    async def initialize(cls):
        '''Загружает необходимую информацию из файлов один раз.'''
        if cls.__initialized:
            return True
        
        logger.info(f'Инициализация шаблонов класса {cls.__name__} внутри функции {__name__}')
        # Загружаем перевод наименований параметров погоды для вывода в клиент
        with open(r"app\bot\weather_processor\data\params_formatted_RU.json", encoding='utf-8', mode='r') as f:
            cls._params_title = json.load(f)
        # Загружаем WMO code
        with open(r"app\bot\weather_processor\data\WMO_code_RU.json", encoding="utf-8", mode="r") as f:
            cls._WMO_RU = json.load(f)

    @classmethod
    async def from_series(cls, data: pd.Series, mode: Duration | None = None) -> str:
        '''Форматирование pd.Series'''
        if mode is not None or (isinstance(mode, Duration) and mode.name != 'CURRENT'):
            raise NotImplemented('Реализован вывод pd.Series только для прогноза погоды сейчас.')
        
        result = [cls._params_title[k].format(round(val, 1)) for k, val in data.items()]
        result = '\n'.join(result)

        return result
    
    @classmethod
    async def from_dataframe(cls, data: pd.DataFrame, mode: Duration) -> str:
        '''Форматирование pd.DataFrame'''
        result = ''

        match mode.name:
            case 'TODAY':
                today = data.index[0].strftime(r'%d.%m.%Y')  # сегодняшнее число

                dates = tuple(map(lambda d: d.strftime(r'%H:00'), data.index))  # время в формате hh:mm    
                data.index = dates
                data = data.map(lambda x: round(x, 1))

                mean = {name: round(data[name].mean(), 1) for name in data.columns}

                data_measures = {
                    'weather_code': cls.WMO_format(int(data['weather_code'].max())),
                    'relative_humidity_2m': mean['relative_humidity_2m'], 
                    'wind_speed_10m': mean['wind_speed_10m'], 
                    'wind_direction_10m': mean['wind_direction_10m'],
                    'wind_direction_word': cls.wind_direction_to_word(mean['wind_speed_10m'])
                }

                data_measures_formatted = temp_today_mean.format(**data_measures)
                result = f'''Погода {today}:

                    {data["temperature_2m"].to_frame(name="температура")}
                    {data_measures_formatted}
                '''
            case 'WEEK':
                dates = tuple(map(lambda d: d.strftime(r'%d.%m.%Y'), data.index))
                data.index = dates
                data = data.map(lambda x: round(x, 1))
                
                ans = {}
                for i, row in data.iterrows():
                    ans.update({i: temp_week.format(
                        row["temperature_2m_min"],
                        row["temperature_2m_max"],
                        row["temperature_2m_mean"],
                        cls.WMO_format(row["weather_code"]).capitalize(),
                        row["precipitation_sum"],
                        row["wind_speed_10m_max"],
                        row["wind_direction_10m_dominant"],
                        cls.wind_direction_to_word(row["wind_direction_10m_dominant"])
                    )})

                result = '\n'.join(('\n———'.join([k, v]) for k, v in ans.items()))

        return result
    
    @classmethod
    def WMO_format(cls, wmo_code: float | int) -> str:
        return cls._WMO_RU[str(int(wmo_code))]

    @classmethod
    def wind_direction_to_word(cls, degrees: float) -> str:
        direction: dict[int, str] = {
            0: "северный",
            45: "северо-восточный",
            90: "восточный",
            135: "юго-восточный",
            180: "южный",
            225: "юго-западный",
            270: "западный",
            315: "северо-западный"
        }

        is_half = (degrees % 45) >= 22.5
        key = (45 * (degrees // 45) + (45 * is_half)) % 360

        return direction[int(key)]
