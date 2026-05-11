from aiogram import Bot
import logging
from aiogram.exceptions import TelegramForbiddenError
from models import User
import random
import asyncio
from parser import get_platonus_grades

logger = logging.getLogger(__name__)

async def update_single_user_grades(bot: Bot, user: User):
    """Обновляет оценки для одного пользователя."""
    try:
        # Небольшая задержка перед стартом, чтобы распределить запросы
        await asyncio.sleep(random.uniform(0.1, 2.0))
        
        # Получаем данные (распаковываем кортеж)
        new_grades, is_cached = await get_platonus_grades(user, force_update=True)

        if isinstance(new_grades, str):
            logger.warning(f"Ошибка обновления для {user.telegram_id}: {new_grades}")
            return

        old_grades = user.cached_grades
        
        if new_grades and old_grades:
            if old_grades != new_grades:
                changes = []
                for subject, new_score in new_grades.items():
                    old_score = old_grades.get(subject)
                    if str(old_score) != str(new_score):
                        if not old_score or old_score == "-":
                            changes.append(f"🆕 <b>{subject}</b>: <b>{new_score}</b>")
                        else:
                            changes.append(f"🔄 <b>{subject}</b>: <s>{old_score}</s> → <b>{new_score}</b>")

                if changes:
                    text = "🔔 <b>Изменения в Платонусе!</b>\n\n" + "\n".join(changes)
                    await bot.send_message(user.telegram_id, text, parse_mode="HTML")
                    
                    user.cached_grades = new_grades
                    await user.save(update_fields=["cached_grades"])
        
        elif new_grades and not old_grades:
            user.cached_grades = new_grades
            await user.save(update_fields=["cached_grades"])

    except TelegramForbiddenError:
        user.is_active = False
        await user.save(update_fields=["is_active"])
        logger.info(f"Юзер {user.telegram_id} заблокировал бота.")
    except Exception as e:
        logger.error(f"Ошибка фоновой проверки {user.telegram_id}: {e}")

async def auto_update_grades_task(bot: Bot):
    """Главная задача планировщика: запускает проверку всех активных юзеров."""
    logger.info("🔄 Запуск фоновой проверки оценок...")
    users = await User.filter(
        get_grades_updates=True, 
        is_active=True, 
        login__not_isnull=True, 
        error_count__lt=5
    ).all()

    if not users:
        logger.info("Нет активных пользователей для обновления.")
        return

    # Запускаем все проверки параллельно.
    # Пока ждет ответ переходит к другому пользователю 
    # Семафор в parser.py сам ограничит одновременные запросы к сайту.
    tasks = [update_single_user_grades(bot, user) for user in users]
    await asyncio.gather(*tasks)
    
    logger.info("✅ Фоновая задача завершена")
