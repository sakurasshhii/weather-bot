from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command
from app.bot.lexic.coordinates import *
from app.bot.keyboards.weather import *
from app.bot.lexic.lexic import WEATHER_RU, WEATHER_DURATION, WEATHER_LOC
import app.bot.functions as bot_func

import logging
import pandas as pd


logger = logging.getLogger(__name__)

api_router = Router()
weather_router = Router()


# Запрос локации для погоды
@weather_router.message(Command(commands=['weather_in_location']))
async def process_ask_location(message: Message):
    await message.answer(
        text=WEATHER_RU['req_loc_txt'],
        reply_markup=req_location_keyboard
    )


@api_router.message(Command(commands=['weather']))
async def process_weather(message: Message, city: str = 'Мурманск', duration: str = 'current'):
    '''
    Главный погодный хэндлер: обрабатывает все запросы на погоду.
    
    :param message: tg update
    :type message: Message
    :param city: Город
    :param duration: Запрос на погоду сейчас / сегодня / недельный
    '''
    result = await bot_func.get_weather_api(message=message, city=city, duration=duration)
    
    await message.answer(
        text=repr(result),
        reply_markup=ReplyKeyboardRemove()
    )


# Ответ на геолокацию: отправка погоды.
@weather_router.message(F.location)
async def process_weather_loc(message: Message):
    await process_weather(message)


# Запрос: введите ваш город
@weather_router.message(F.text == WEATHER_RU['other_loc_btn'])
async def process_other_location(message: Message):
    await message.answer(WEATHER_RU['other_loc'])


# Ответ на название города: отправка погоды.
@weather_router.message(F.text.lower().in_(city_names))
async def process_weather_other(message: Message):
    await process_weather(message, message.text)

@weather_router.callback_query(F.data.in_(WEATHER_DURATION.keys()))
async def process_duration(callback: CallbackQuery):
    await process_weather(callback, city='Москва', duration=callback.data)
    