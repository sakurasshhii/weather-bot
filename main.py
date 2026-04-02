import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
# from aiogram.enums import ParseMode  # parse_mode=ParseMode.HTML
from config_data.config import Config, load_config
from app.bot.keyboards import set_main_menu
from app.bot.handlers import (
    start_router,
    api_router,
    weather_router,
    unexpected_router
)


logger = logging.getLogger(__name__)


async def main() -> None:
    '''
    Функция конфигурирования и запуска бота
    '''
    logger.info('Starting bot...')

    # Загружаем Config
    config: Config = load_config()
    
    # Конфигурируем логирование
    logging.basicConfig(
        level=config.log.level,
        format=config.log.format
    )

    session = AiohttpSession(proxy=config.proxy.proxy_url)
    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.bot_token,
        session=session,
        default=DefaultBotProperties()
    )
    dp = Dispatcher()  # добавить объект хранилища storage

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # регистрируем роутеры
    logger.info('Include routers...')

    dp.include_routers(
        start_router,
        api_router,
        weather_router,
        unexpected_router
    )

    logger.info('start polling...')

    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
