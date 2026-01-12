import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

import app.bot.handlers


logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.bot_token)
    dp = Dispatcher()

    dp.include_routers(
        app.bot.handlers.router,
        app.bot.handlers.api_router,
        app.bot.handlers.unexpected_router
    )
    
    logging.info('start polling...')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())