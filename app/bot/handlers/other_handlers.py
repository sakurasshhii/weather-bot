from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart


unexpected_router = Router()


@unexpected_router.message()
async def unexpected_command(message: Message):
    await message.reply('unlknown bla bla')
