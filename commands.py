from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    # Создаем список из команд и их описаний
    commands = [
        BotCommand(command="start", description="Перезапустить бота"),
        BotCommand(command="login", description="🔑 Войти в Платонус"),
        BotCommand(command="grades", description="📊 Мои оценки"),
        BotCommand(command="help", description="❓ Как пользоваться ботом")
    ]

    # Отправляем этот список серверам Telegram
    await bot.set_my_commands(commands)
