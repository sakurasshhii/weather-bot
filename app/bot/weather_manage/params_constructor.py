import json
import logging
from dataclasses import dataclass
from datetime import timedelta, datetime, date


logger = logging.getLogger(__name__)
with open(r"app\bot\functions\params_duration.json", encoding="utf-8", mode="r") as f:
    params_duration = json.load(f)


@dataclass
class Params:
    __params_temp = params_duration
    _utc_offset = timedelta(hours=2)

    latitude: float
    longitude: float

    @classmethod
    async def hourly_format(cls):
        'Рассчитывает временные рамки на день'
        now = datetime.now() + cls._utc_offset
        end_hour = datetime(year=now.year, month=now.month, day=now.day + 1, hour=0)
        end_hour += cls._utc_offset
        return now.strftime(r'%Y-%m-%dT%H:00'), end_hour.strftime(r'%Y-%m-%dT%H:00')

    @classmethod
    async def daily_format(cls):
        'Рассчитывает временные рамки на неделю'
        now = date.today()
        end_day = date(year=now.year, month=now.month, day=now.day + 7)
        logger.info(f"time spread for one week: {now.isoformat()} to {end_day.isoformat()}")
        return now.isoformat(), end_day.isoformat()

    async def get_params(self, duration):
        'Генерирует параметры для запроса погоды'
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": "auto"
        }
        params.update(self.__class__.__params_temp[duration])

        match duration:
            case "today":
                hour_st, hour_en = await self.hourly_format()
                params.update({
                    "start_hour": hour_st,
                    "end_hour": hour_en
                })
            case "week":
                date_st, date_en = await self.daily_format()
                params.update({
                    "start_date": date_st,
                    "end_date": date_en
                })

        return params
    