from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import F
from app.bot.lexic import city_names



class IsValidCity(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            return message.text.lower() in city_names
        return False
