import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from bot_handler import router
from db_api import init_db
from commands import set_bot_commands

async def main():
    init_db()  # Инициализируем базу данных при старте бота
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await set_bot_commands(bot)  # Устанавливаем команды бота в Telegram
    print("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(main())