from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart


router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('hi')

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('i cant help you as well as i cant help myself')
