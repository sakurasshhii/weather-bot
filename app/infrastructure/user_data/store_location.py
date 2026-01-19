import json
import os
import logging
from typing import Any


__all__ = ['update_data', 'add_user', 'del_user', 'update_user_info', 'get_user']

logger = logging.getLogger(__name__)

PATH = os.path.normpath(r"app\infrastructure\user_data\data.json")


async def load_data():
    with open(file=PATH, mode="r+", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


async def update_data(data: dict) -> None:
    with open(file=PATH, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    logging.info('data updated...')


async def add_user(user_id: int | str, latitude: float | None = None, longitude: float | None = None) -> None:
    data = await load_data()
    user_id = str(user_id)
    if user_id not in data:
        data.setdefault(user_id, {"coordinates": None})
    if latitude and longitude:
        data[user_id]["coordinates"] = {
            "latitude": latitude,
            "longitude": longitude
        }

    await update_data(data)


async def update_user_info(user_id: int | str, **kwargs: Any):
    data = await load_data()
    user_id = str(user_id)
    if user_id not in data:
        await add_user(user_id)
    if "coordinates" in kwargs:
        kwargs["coordinates"] = {
            "latitude": kwargs["coordinates"][0],
            "longitude": kwargs["coordinates"][1]
        }
    data[user_id].update(kwargs)

    await update_data(data)


async def get_user(user_id: int | str):
    data = await load_data()

    return data[str(user_id)]


async def del_user(user_id: int | str) -> None:
    data = await load_data()
    user_id = str(user_id)
    if user_id in data:
        del data[user_id]

        await update_data(data)
