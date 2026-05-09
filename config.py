import os

from dotenv import load_dotenv

# Подгружаем данные из .env
load_dotenv()
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
URL=os.getenv("SERVER_URL")
FERNET_KEY=os.getenv("FERNET_KEY").encode()
