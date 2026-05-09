import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from bot_handler import router
from commands import set_bot_commands
from config import TELEGRAM_TOKEN


class NoSleepFilter(logging.Filter):
    def filter(self, record):
        # Превращаем сообщение в нижний регистр и ищем слово "sleep"
        # Если слова нет -> возвращаем True (пропускаем в лог)
        # Если слово есть -> возвращаем False (блокируем сообщение)
        return "Sleep" not in record.getMessage().lower()

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
        handlers=[console_handler, file_handler],
        force=True  # Это нужно, чтобы переопределить базовую конфигурацию, если она уже была настроена
    )
    logging.getLogger("aiogram").addFilter(NoSleepFilter())
    logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def init_db():
    await Tortoise.init(
        db_url='sqlite://database.db',
        modules={'models' : ["models"]}
    )
    await Tortoise.generate_schemas()
    logger.info("БД иницализировался!")

async def main():
    setup_logging()
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
        )
    finally:
        Tortoise.close_connections()
        logger.info("Соединеие с БД закрыто")

if __name__ == "__main__":
    asyncio.run(main())
