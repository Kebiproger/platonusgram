import asyncio
import logging

from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from bot_handler import router
from commands import set_bot_commands
from config import TELEGRAM_TOKEN, setup_logging,init_db



async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    await init_db()  # Инициализируем базу данных при старте бота
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await set_bot_commands(bot)  # Устанавливаем команды бота в Telegram
    logger.info("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await asyncio.gather(
            # Чтоб запускать много процессов одновременно
            dp.start_polling(bot)
            # 1. Создаем семафор на 5 одновременных подключений.
# (Лучше всего инициализировать его при старте бота, там же, где и базу данных)
        )
    finally:
        Tortoise.close_connections()
        logger.info("Соединеие с БД закрыто")

if __name__ == "__main__":
    asyncio.run(main())
