from parser import get_platonus_grades
import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from bot_handler import router

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    print("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())