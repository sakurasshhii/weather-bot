import json
import pandas as pd


# Загружаем перевод наименований параметров погоды для вывода в клиент
with open(r"app\bot\functions\params_formatted_RU.json", encoding='utf-8', mode='r') as f:
    measure = json.load(f)

# Загружаем параметры запроса
with open(r"app\bot\functions\params_duration.json", encoding='utf-8', mode='r') as f:
    params = json.load(f)

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


'''
0° / 360°: Север (дует с севера).
90°: Восток (дует с востока).
180°: Юг (дует с юга).
270°: Запад (дует с запада). '''

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

    pd_data["temperature_2m"] = [round(x, 1) for x in pd_data["temperature_2m"]]  # температура в формате xx.x

    mean = {}
    for title in ['relative_humidity_2m', 'wind_speed_10m', 'wind_direction_10m']:
        mean.update({title: pd_data[title].mean()})

    meanes = map(lambda val: str(round(val, 1)), mean.values())  # погодные показатели, округленные до десятых
    meanes = 'Относительная влажность {}%\nВетер {} м/c\nНаправление ветра {}°'.format(*meanes)

    ans = f'''
Погода {today}:

{pd_data["temperature_2m"].to_frame(name="температура")}

{meanes}
'''

    return ans


# Week format
async def str_format_week(pd_data: pd.DataFrame) -> str:
    dates = tuple(map(lambda d: d.strftime(r'%d.%m.%Y'), pd_data.index))
    pd_data.index = dates

    temp = '''
Температура воздуха от {}° до {}°, в среднем, {}°
Ожидается {}, осадки {}мм
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
