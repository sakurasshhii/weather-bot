from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from app.bot.lexic.lexic import MENU_RU


start_router = Router()
unexpected_router = Router()


@start_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(MENU_RU['/start'])


@start_router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(MENU_RU['/help'])

@unexpected_router.message()
async def unexpected_command(message: Message):
    await message.reply(MENU_RU['/unexpected_message'])

