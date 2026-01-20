import json
import pandas as pd


# Загружаем перевод наименований параметров погоды для вывода в клиент
with open(r"app\bot\functions\params_formatted_RU.json", encoding='utf-8', mode='r') as f:
    measure = json.load(f)


# Current format
async def str_format_current(pd_ser: pd.Series[float]) -> str:
    ans = [measure[k].format(round(val, 1)) for k, val in pd_ser.items()]
    ans = '\n'.join(ans)

    return ans


# Today format
async def str_format_today(pd_data: pd.DataFrame) -> str:
    mean = {}
    for title in ['relative_humidity_2m', 'wind_speed_10m', 'wind_direction_10m']:
        mean.update({title: pd_data[title].mean()})

    today = pd_data.index[0].strftime('%d.%m.%Y')  # сегодняшнее число

    dates = tuple(map(lambda d: d.strftime('%H:00'), pd_data.index))  # время в формате hh:mm    
    pd_data.index = dates

    pd_data["temperature_2m"] = [round(x, 1) for x in pd_data['temperature_2m']]  # температура в формате xx.x

    meanes = map(lambda val: str(round(val, 1)), mean.values())  # погодные показатели, округленные до десятых
    meanes = 'Относительная влажность {}%\nВетер {} м/c\nНаправление ветра {}°'.format(*meanes)

    ans = f'''
Погода {today}:

{pd_data["temperature_2m"].to_frame(name='температура')}

{meanes}
'''

    return ans


# Week format
async def str_format_week(pd_data: pd.DataFrame) -> str:
    pass


# Wind direction in words
async def wind_direction_to_word(degrees: float) -> str:
    pass
