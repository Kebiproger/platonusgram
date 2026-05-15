import asyncio
import logging

from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from bot.bot_handler import public_router, private_router
from bot.commands import set_bot_commands
from backend.config import TELEGRAM_TOKEN, setup_logging,init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from backend.tasks import auto_update_grades_task
from datetime import timezone, timedelta

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
        hour="10-22/3", # 8:00-20:00 every 3 hours 
        minute="0",
        kwargs={'bot': bot},
        jitter=600
    )

    
    
    # Запускаем планировщик
    scheduler.start()
    logging.info("APScheduler успешно запущен (Режим: 08:00 - 20:00)!")
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
