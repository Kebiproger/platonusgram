import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from bot_handler import router
from db_api import init_db
from commands import set_bot_commands
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s(%(lineno)d) - %(message)s"
    )

    # 1. Хэндлер для вывода в консоль (черный экран)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 2. Хэндлер для записи в файл (максимум 5 МБ, храним 3 штуки)
    file_handler = RotatingFileHandler(
        "bot_logs.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Применяем настройки ко всему проекту
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

# Создаем личный логгер для этого файла
logger = logging.getLogger(__name__)

async def main():
    setup_logging()
    init_db()  # Инициализируем базу данных при старте бота
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await set_bot_commands(bot)  # Устанавливаем команды бота в Telegram
    logger.info("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(main())