import contextlib
import json
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from crypto import  fernet_encrypt_password, js_decrypt_password
from keyboards import get_login_kb, get_main_kb, get_subjects_kb, get_back_to_subjects_kb
from models import User
from parser import get_platonus_grades
from datetime import timezone, timedelta, datetime
from zoneinfo import ZoneInfo
import hashlib

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("help"))
async def help(message: Message):
    return await message.answer('''
    <b>🎓 Справочный центр бота</b>

Я независимый бот-ассистент, который помогает быстро узнавать оценки из Платонуса без необходимости постоянно вводить логин и пароль.

<b>🛠 Основные команды:</b>
/start — Перезапустить бота
/login — Авторизоваться (или обновить пароль)
/grades — Узнать текущие оценки

<b>❓ Частые вопросы (FAQ):</b>

<b>1. Бот выдает ошибку авторизации. Что делать?</b>
Скорее всего, ты изменил пароль в самом Платонусе. Просто нажми /login и введи данные заново.

<b>2. Почему бот так долго грузит оценки?</b>
Я запрашиваю данные напрямую с серверов университета. Если Платонус перегружен или "лежит", мне тоже требуется время на ответ. Пожалуйста, подожди 10-15 секунд.

<b>3. Это безопасно? Вы украдете мой пароль?</b>
Бот шифрует пароли современными алгоритмами (AES) и использует их только для автоматического входа на портал. Но помни: проект неофициальный, используй его на свое усмотрение.Подробнее в https://github.com/Kebiproger/platonusgram
.
''', parse_mode="HTML",disable_web_page_preview=True)

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Проверяем, есть ли юзер в БД
    user = await User.get_or_none(telegram_id=message.from_user.id)

    if user:
        text = "✅ С возвращением! Ты уже в системе. Можешь проверять оценки."
        kb = get_main_kb()
    else:
        text = ('''👋 Привет! Я — твой независимый ассистент для учебы.

Я избавлю тебя от необходимости постоянно проверять портал. Я буду сам следить за твоим журналом и расписанием, а ты сможешь сфокусироваться на главном.

⚠️ Проект создан студентами для студентов и не является официальным ботом университета.

Чтобы начать получать уведомления об оценках, нажми кнопку ниже и авторизуйся в системе (это нужно сделать всего один раз):
''')
        kb = get_login_kb()

    await message.answer(text, reply_markup=kb)

@router.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    # 🛡 ГАРАНТИЯ ДЛЯ PYLANCE: Если автора или данных нет — игнорируем
    if not message.from_user or not message.web_app_data:
        return

    # 1. Достаем ту самую JSON-строку, которую мы отправили из JS
    raw_data = message.web_app_data.data

    try:
    # 2. Превращаем строку в словарь Python
        parsed_data = json.loads(raw_data)
    except json.JSONDecodeError:
        logger.warning(f"Получен кривой JSON от {message.from_user.id}: {raw_data}")
        return await message.answer("❌ Ошибка передачи данных. Попробуйте снова.")

    if parsed_data.get("action") == "login":
        encrypted_pass = parsed_data.get("password")
        platonus_login = parsed_data.get("login")
        if not platonus_login or not encrypted_pass:
            await message.answer("❌ Ошибка: Данные неполные. Пожалуйста, очистите кэш Телеграма и попробуйте снова.")
            return

        try:
            real_password = js_decrypt_password(encrypted_pass)
        except Exception as e:
            logger.error(f"Ошибка расшифровки пароля WebApp: {e}")
            return await message.answer("❌ Ошибка безопасности. Пароль поврежден при передаче.")
        # user не нужен
        encrypted_password = fernet_encrypt_password(real_password)

        
        user, created = await User.update_or_create(
            telegram_id=message.from_user.id,
            defaults={
                "login": platonus_login,
                "password_enc": encrypted_password
            }
        )

        if created:
            await message.answer("Пароль успешно получен и зашифрован!Если хочешь узнать оценки, нажми '🎓 Узнать оценки',если хочешь повторно логиниться то нажми команду /login", reply_markup=get_main_kb())
        else:
            await message.answer('С возвращением! Я обновил твои данные в базе, если они изменились.', reply_markup=get_main_kb())


@router.message(Command("login"))
async def login_cmd(message: Message):
    login_kb = get_login_kb()
    await message.answer("Нажми на кнопку ниже, чтобы безопасно ввести пароль:", reply_markup=login_kb)

@router.message(F.text == "📊 Мои оценки")
@router.message(Command("grades"))
@router.callback_query(F.data == "grades")
async def cmd_grades(event: CallbackQuery | Message):
    user_id = event.from_user.id
    logger.info(f"Юзер {user_id} запросил оценки.")
    force_update = False
    user = await User.get_or_none(telegram_id=user_id)
    if not event.from_user or not user.login:
        msg_text = "❌ Ошибка авторизации. Нажми 'Войти'."
        if isinstance(event, Message):
            await event.answer(msg_text, reply_markup=get_login_kb())
        else:
            await event.message.answer(msg_text, reply_markup=get_login_kb())
        return

    if isinstance(event, CallbackQuery) and event.data == "grades":
        
        # --- ПРОВЕРКА КУЛДАУНА (Только для принудительного обновления) ---
        if user.grades_updated_at:
            now = datetime.now(timezone.utc)
            time_passed = now - user.grades_updated_at
            
            if time_passed < timedelta(minutes=15):
                minutes_left = 15 - int(time_passed.total_seconds() / 60)
                # Выкидываем красную плашку и ПРЕРЫВАЕМ функцию!
                await event.answer(f"⏳ Слишком часто! Повтори попытку через {minutes_left} мин.", show_alert=True)
                return
            
        force_update = True
        await event.answer("🔄 Обновляю данные с сервера...") 
        msg = await event.message.edit_text("⏳ Подключаюсь к Платонусу...")

    elif isinstance(event, CallbackQuery) and event.data == "back_to_subjects":
        await event.answer() # Убираем часики на кнопке
        msg = await event.message.edit_text("⏳ Загружаю меню предметов...")   
    # СЦЕНАРИЙ В: Пользователь нажал нижнюю кнопку меню
    else:
        msg = await event.answer("⏳ Загружаю меню предметов...")

    # Берем время из базы данных (когда реально обновились оценки)
    time_str = "неизвестно"
    if user.grades_updated_at:
        time_str = user.grades_updated_at.astimezone(ZoneInfo("Asia/Almaty")).strftime("%H:%M")

    try:
        grades_dict, is_cached = await get_platonus_grades(user, force_update=force_update)
        
        intro_text = "📊 <b>Ваши предметы:</b>\n<i>Выберите номер предмета внизу.</i>\n\n"
        for index, subject_name in enumerate(grades_dict.keys(), start=1):
            intro_text += f"<b>{index}.</b> {subject_name}\n"
        
        if is_cached:
            intro_text += f"\n<i>(Взято из кэша. Обновлено в {time_str})</i>"
        else:
            intro_text += "\n<i>(Данные свежие, только что спарсены с Платонуса)</i>"
        
        await msg.edit_text(intro_text, parse_mode="HTML", reply_markup=get_subjects_kb(grades_dict))

    except Exception as e:
        logger.error(f"Не смог спарсить оценки для {user_id}: {e}", exc_info=True)
        # Если не удалось отредактировать (например, из-за лимитов или ошибок HTML), отправляем новым сообщением
        with contextlib.suppress(BaseException):
            await msg.delete()
        await event.bot.send_message(chat_id=user_id, text="⚠️ Ошибка при получении оценок.", parse_mode="HTML")

@router.callback_query(F.data.startswith("subj_"))
async def show_subject_details(callback: CallbackQuery):
    user = await User.get_or_none(telegram_id=callback.from_user.id)
    if not user or not user.cached_grades:
        await callback.answer("❌ Данные устарели. Нажмите 'Мои оценки' еще раз.", show_alert=True)
        return

    # Достаем хэш предмета из callback_data (например, отрезаем "subj_")
    clicked_hash = callback.data.replace("subj_", "")
    
    # Так как мы сохранили кэш как JSON, достаем его
    # (Если cached_grades это строка, сделай json.loads(user.cached_grades))
    grades_dict = user.cached_grades 

    # Ищем предмет, чей хэш совпадает с нажатым
    target_subject = None
    target_grades = None
    for subj_name, grades_text in grades_dict.items():
        if hashlib.md5(subj_name.encode()).hexdigest()[:10] == clicked_hash:
            target_subject = subj_name
            target_grades = grades_text
            break

    if target_subject:
        # Формируем красивый текст для одного предмета
        detail_text = f"📚 <b>{target_subject}</b>\n\n{target_grades}"
        # Отправляем текст с кнопкой НАЗАД
        await callback.message.edit_text(detail_text, parse_mode="HTML", reply_markup=get_back_to_subjects_kb())
    else:
        await callback.answer("❌ Предмет не найден.", show_alert=True)


# --- НОВЫЙ ХЭНДЛЕР ДЛЯ КНОПКИ "НАЗАД" ---
@router.callback_query(F.data == "back_to_subjects")
async def go_back_to_menu(callback: CallbackQuery):
    user = await User.get_or_none(telegram_id=callback.from_user.id)
    
    if not user or not user.cached_grades:
        # Если кэша почему-то нет (например, стерли БД), просим нажать нижнюю кнопку
        await callback.message.edit_text("❌ Данные устарели. Нажми '📊 Мои оценки' внизу экрана.")
        return

    # 4. ДОСТАЕМ ДАННЫЕ НАПРЯМУЮ ИЗ БД (Никакого парсера!)
    # Если ты сохранял словарь через json.dumps, то теперь распаковываем его:
    grades_dict = user.cached_grades

    # 5. Формируем красивое время (как обычно)
    time_str = "неизвестно"
    if user.grades_updated_at:
        almaty_tz = ZoneInfo("Asia/Almaty")
        utc_time = user.grades_updated_at.replace(tzinfo=timezone.utc)
        time_str = utc_time.astimezone(almaty_tz).strftime("%H:%M")
        
    text = f"📊 <b>Ваши предметы:</b>\n<i>Выберите номер предмета внизу.</i>\n\n"   
    # Просто заново отрисовываем главное меню предметов из кэша
    for index, subject_name in enumerate(grades_dict.keys(), start=1):
        text += f"<b>{index}.</b> {subject_name}\n"
        
    text += f"\n<i>(Взято из кэша. Обновлено в {time_str})</i>"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=get_subjects_kb(grades_dict))


