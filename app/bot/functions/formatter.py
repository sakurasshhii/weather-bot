import json


with open(r"app\bot\functions\measure_RU.json", encoding='utf-8', mode='r') as f:
    measure = json.load(f)


async def str_format_current(pd_ser):
    ans = [measure[k].format(val) for val, k in pd_ser.items()]
    ans = '\n'.join(ans)

    return ans


async def str_format_today(pd_data):
    mean = {}
    for title in ['relative_humidity_2m', 'wind_speed_10m', 'wind_direction_10m']:
        mean.update({title: pd_data[title].mean()})

    today = pd_data.index[0].strftime('%d.%m.%Y')

    dates = pd_data.index
    dates = map(lambda d: d.strftime('%H:00'), dates)
    pd_data.index = dates

    meanes = 'Относительная влажность {}%\nВетер {} м/c\nНаправление ветра {}°'.format(*map(str, mean.values()))

    ans = f'''
Погода {today}:

{pd_data["temperature_2m"].to_frame(name='температура')}

{meanes}
'''

    return ans
