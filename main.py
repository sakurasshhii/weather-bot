import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
import app.bot.handlers as handlers
import app.bot.keyboards as keyboards


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

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()  # добавить объект хранилища storage

    # Настраиваем кнопку Menu
    await keyboards.set_main_menu(bot)

    # регистрируем роутеры
    logger.info('Include routers...')

    dp.include_routers(
        handlers.start_router,
        handlers.api_router,
        handlers.unexpected_router
    )

    logger.info('start polling...')

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
