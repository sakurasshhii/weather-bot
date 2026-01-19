from aiogram import Router
from aiogram.types import Message
from app.bot.lexic.lexic import MENU_ANS_RU

unexpected_router = Router()


@unexpected_router.message()
async def unexpected_command(message: Message):
    await message.reply(MENU_ANS_RU['/unexpected_message'])
