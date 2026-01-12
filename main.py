import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

import app.bot.handlers


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.bot_token)
    dp = Dispatcher()

    dp.include_routers(
        app.bot.handlers.router,
        app.bot.handlers.api_router,
        app.bot.handlers.unexpected_router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())