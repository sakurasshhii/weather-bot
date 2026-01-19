import json
import os
import logging


__all__ = ['load_data', 'update_data', 'add_user', 'del_user']

logger = logging.getLogger(__name__)

PATH = os.path.normpath(r"app\infrastructure\user_info\data.json")


async def load_data():
    with open(file=PATH, mode="r+", encoding="utf-8") as f:
        try:
            return await json.load(f)
        except json.JSONDecodeError:
            return {}


async def update_data(data: dict) -> None:
    with open(file=PATH, mode="r+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    logging.info('data updated...')


async def add_user(user_id: int, latitude: float | None = None, longitude: float | None = None) -> None:
    data = await load_data()
    data.setdefault(user_id, {"coordinates": {}})
    if latitude and longitude:
        data[user_id]["coordinates"] = {
            "latitude": latitude,
            "longitude": longitude
        }

    await update_data(data)


async def del_user(user_id: int) -> None:
    data = await load_data()
    if user_id in data:
        del data[user_id]

        await update_data(data)
