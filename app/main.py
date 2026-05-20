import asyncio
import logging

from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from app.bot.bot_handler import public_router, private_router
from app.bot.commands import set_bot_commands
from app.core.config import TELEGRAM_TOKEN, setup_logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.tasks import auto_update_grades_task
from datetime import timezone, timedelta
from app.db.db_config import init_db
import os

async def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # Проверка наличия приватного ключа (пункт 4 стабильности)
    if not os.path.exists("private.pem"):
        logger.error("❌ Файл 'private.pem' не найден! Бот не сможет расшифровывать пароли из WebApp.")
        return

    await init_db(generate_schemas=False)  # Инициализируем БД без автогенерации схем (используем миграции)
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(public_router)
    dp.include_router(private_router)
    await set_bot_commands(bot)  # Устанавливаем команды бота в Telegram
    logger.info("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)

    kz_tz=timezone(timedelta(hours=5))
    #  --- ⚙️ НАСТРОЙКА APSCHEDULER ---
    # Создаем асинхронный планировщик
    scheduler = AsyncIOScheduler(timezone=kz_tz)
    
    # Добавляем задачу. 
    # trigger='interval' означает повторение через промежуток времени.
    # kwargs - это аргументы, которые мы передаем в функцию test_beep_task
    scheduler.add_job(
        auto_update_grades_task, 
        trigger='cron',
        # trigger='interval',
        hour="8-22/2", # 10:00-22:00 every 3 hours 
        minute=15,
        kwargs={'bot': bot},
        jitter=600
    )
    
    # Запускаем планировщик
    scheduler.start()
    logging.info("APScheduler успешно запущен (Режим: 10:00 - 22:00)!")
    try:
        logging.info("Бот запущен и слушает обновления...")
        await asyncio.gather(
            # Чтоб запускать много процессов одновременно
            dp.start_polling(bot),
            
            # 1. Создаем семафор на 5 одновременных подключений.
# (Лучше всего инициализировать его при старте бота, там же, где и базу данных)
        )
    finally:
        scheduler.shutdown()
        Tortoise.close_connections()
        logger.info("Соединеие с БД закрыто")

if __name__ == "__main__":
    asyncio.run(main())
