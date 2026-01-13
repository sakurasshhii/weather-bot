from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart


start_router = Router()


@start_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('hi')


@start_router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('i cant help you as well as i cant help myself')
