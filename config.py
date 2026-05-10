import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from tortoise import Tortoise
# Подгружаем данные из .env
load_dotenv()
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
URL=os.getenv("SERVER_URL")
FERNET_KEY=os.getenv("FERNET_KEY").encode()

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
        db_url='sqlite://database.db?wal=true',
        modules={'models' : ["models"]}
    )
    await Tortoise.generate_schemas()
    conn = Tortoise.get_connection("default")
    
    # Отправляем "сырые" команды SQLite для настройки
    await conn.execute_query("PRAGMA journal_mode=WAL;")
    await conn.execute_query("PRAGMA synchronous=NORMAL;") # <- Секретный буст скорости
    
    logger.info("База данных Tortoise инициализирована. Режим WAL включен!")