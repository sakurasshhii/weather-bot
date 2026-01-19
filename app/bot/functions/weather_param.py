import json
from datetime import datetime, date, UTC, timedelta


utc_offset = timedelta(hours=3)

with open(r"app\bot\functions\params_duration.json", encoding="utf-8", mode="r") as f:
    params_duration = json.load(f)


# Рассчитывает временные рамки на день
async def hourly_format():
    now = datetime.now()
    end_hour = datetime(year=now.year, month=now.month, day=now.day + 1, hour=0)
    end_hour += utc_offset
    return now.strftime(r'%Y-%m-%dT%H:00'), end_hour.strftime(r'%Y-%m-%dT%H:00')


# Рассчитывает временные рамки на неделю
async def daily_format():
    now = date.today()
    end_day = date(year=now.year, month=now.month, day=now.day + 7)
    return now.isoformat(), end_day.isoformat()


# Формирует список параметров для API-запроса
async def get_params(latitude: float, longitude: float, duration: str):
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
    match duration:
        case "today":
            hour_st, hour_en = await hourly_format()
            params.update({
                "start_hour": hour_st,
                "end_hour": hour_en
            })
        case "week":
            date_st, date_en = await daily_format()
            params.update({
                "start_date": date_st,
                "end_date": date_en
            })

    return params
