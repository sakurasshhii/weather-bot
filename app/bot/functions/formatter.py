import json
import pandas as pd
import logging


logger = logging.getLogger(__name__)

# Загружаем перевод наименований параметров погоды для вывода в клиент
with open(r"app\bot\functions\params_formatted_RU.json", encoding='utf-8', mode='r') as f:
    measure = json.load(f)


# Загружаем WMO code
with open(r"app\bot\functions\WMO_code_RU.json", encoding="utf-8", mode="r") as f:
    WMO_RU = json.load(f)


# Wind direction in words
def wind_direction_to_word(degrees: float) -> str:
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
    degrees = int(degrees) % 360

    full = degrees // 45
    n = (full + 1, full)[abs(full - degrees) < abs(full - degrees + 45)]
    
    return direction[45 * n]


# WMO decode
def WMO_format(code: int | float) -> str:
    return WMO_RU[str(int(code))]


# Current format
async def str_format_current(pd_ser: pd.Series[float]) -> str:
    ans = [measure[k].format(round(val, 1)) for k, val in pd_ser.items()]
    ans = '\n'.join(ans)

    return ans


# Today format
async def str_format_today(pd_data: pd.DataFrame) -> str:
    today = pd_data.index[0].strftime(r'%d.%m.%Y')  # сегодняшнее число

    dates = tuple(map(lambda d: d.strftime(r'%H:00'), pd_data.index))  # время в формате hh:mm    
    pd_data.index = dates
    pd_data = pd_data.map(lambda x: round(x, 1))

    mean = {name: round(pd_data[name].mean(), 1) for name in pd_data.columns}

    temp = '''
{}

Относительная влажность {}%
Ветер {} м/c
Направление ветра {}° ({})
    '''

    meanes_dt = temp.format(
        WMO_format(int(pd_data['weather_code'].max())),
        mean['relative_humidity_2m'], 
        mean['wind_speed_10m'], 
        mean['wind_direction_10m'],
        wind_direction_to_word(mean['wind_speed_10m'])
    )

    ans = f'''
Погода {today}:

{pd_data["temperature_2m"].to_frame(name="температура")}
{meanes_dt}
'''

    return ans


# Week format
async def str_format_week(pd_data: pd.DataFrame) -> str:
    dates = tuple(map(lambda d: d.strftime(r'%d.%m.%Y'), pd_data.index))
    pd_data.index = dates

    temp = '''
Температура воздуха от {}° до {}°, в среднем, {}°
{}, осадки {}мм
Ветер {}м/с, {}° ({})
'''
    pd_data = pd_data.map(lambda x: round(x, 1))
    
    ans = {}
    for i, row in pd_data.iterrows():
        ans.update({i: temp.format(
            row["temperature_2m_min"],
            row["temperature_2m_max"],
            row["temperature_2m_mean"],
            WMO_format(row["weather_code"]).lower(),
            row["precipitation_sum"],
            row["wind_speed_10m_max"],
            row["wind_direction_10m_dominant"],
            wind_direction_to_word(row["wind_direction_10m_dominant"])
        )})
    
    return '\n'.join(('\n———'.join([k, v]) for k, v in ans.items()))
