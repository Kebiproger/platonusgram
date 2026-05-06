from dotenv import load_dotenv
import os

# Подгружаем данные из .env
load_dotenv()
# LOGIN = os.getenv("PLATONUS_LOGIN")
# PASSWORD = os.getenv("PLATONUS_PASSWORD")
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID=os.getenv("TELEGRAM_CHAT_ID")
URL=os.getenv("SERVER_URL")
FERNET_KEY=os.getenv("FERNET_KEY").encode()