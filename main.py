from parser import get_platonus_grades
import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from bot_handler import router
from web_server import setup_web_app
from aiohttp import web

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("🤖 Бот запущен. Ожидание команд...")
    await bot.delete_webhook(drop_pending_updates=True)
    app = setup_web_app()
    app['bot'] = bot  # Сохраняем объект бота в контексте приложения для доступа из обработчиков
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await asyncio.gather(
        dp.start_polling(bot),
        site.start()
    )

if __name__ == "__main__":
    asyncio.run(main())