from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from app.bot.lexic.lexic import MENU_ANS_RU
from app.bot.keyboards.weather import duration_kboard
# import app.infrastructure.user_info as data
from app.infrastructure.user_info import add_user

import logging


start_router = Router()
logger = logging.getLogger(__name__)


# /start
@start_router.message(CommandStart())
async def process_start_command(message: Message):
    await add_user(message.from_user.id)
    await message.answer(MENU_ANS_RU['/start'])

# /help
@start_router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(MENU_ANS_RU['/help'])

# /get_weather
@start_router.message(Command(commands=['get_weather']))
async def process_start_weather(message: Message):
    await message.answer(
        text=(MENU_ANS_RU['/get_weather']),
        reply_markup=duration_kboard
    )
# убрать, сделать: weather_current, weather_today, weather_week
