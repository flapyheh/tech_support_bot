import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.user import user_router
from bot.handlers.operator import operator_router
from bot.middlewares.Throttling import ThrottlingMiddleware
from bot.middlewares.OperatorMiddleware import OperatorMiddleware
from bot.config.config import settings
from bot.db.query.orm import create_tables, insert_all_operators
from bot.bot_module import bot

logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main() -> None:
    logger.info("Starting bot...")
    # Инициализируем хранилище
    storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    
    logger.info('Creating DB tables...')
    await create_tables()
    
    logger.info('Adding all operators')
    await insert_all_operators(settings.bot.ADMIN_IDS)
    
    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    dp.include_routers(operator_router, user_router)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    dp.update.middleware(ThrottlingMiddleware())
    operator_router.message.outer_middleware(OperatorMiddleware())

    # Запускаем поллинг
    try:
        await dp.start_polling(
            bot, 
            admin_ids=settings.bot.ADMIN_IDS
        )
    except Exception as e:
        logger.exception(e)