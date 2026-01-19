'''
Файл с функциями для форматирования pd.Series и pd.DataFrame
для последующего вывода пользователю в сообщении тг
'''
from datetime import datetime, date, UTC, timedelta


utc_offset = timedelta(hours=3)

async def hourly_format():
    now = datetime.now()
    end_hour = datetime(year=now.year, month=now.month, day=now.day + 1, hour=0)
    end_hour += utc_offset
    return now.strftime(r'%Y-%m-%dT%H:00'), end_hour.strftime(r'%Y-%m-%dT%H:00')


async def daily_format():
    now = date.today()
    end_day = date(year=now.year, month=now.month, day=now.day + 7)
    return now.isoformat(), end_day.isoformat()
