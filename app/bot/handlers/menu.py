from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from app.bot.lexic.lexic import MENU_ANS_RU
import app.infrastructure.user_data as data

import logging


start_router = Router()
logger = logging.getLogger(__name__)


# /start
@start_router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user:
        await data.add_user(message.from_user.id)
    else:
        logger.warning('Нет доступа к id пользователя')
        
    await message.answer(MENU_ANS_RU['/start'])

# /help
@start_router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(MENU_ANS_RU['/help'])
