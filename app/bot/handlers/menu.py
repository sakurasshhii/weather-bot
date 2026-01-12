from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart


start_router = Router()

@start_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('hi')