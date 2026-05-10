import contextlib
import json
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from crypto import  fernet_encrypt_password, js_decrypt_password
from keyboards import get_login_kb, get_main_kb
from models import User
from parser import get_platonus_grades

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
        # 4. Расшифровываем!

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
            await message.answer('С возвращением! Я обновил твои данные в базе, если они изменились.')


@router.message(Command("login"))
async def login_cmd(message: Message):
    login_kb = get_login_kb()
    await message.answer("Нажми на кнопку ниже, чтобы безопасно ввести пароль:", reply_markup=login_kb)

@router.message(Command("grades"))
@router.callback_query(F.data == "grades")
async def cmd_grades(event: CallbackQuery | Message):
    if not event.from_user:
        return
    user_id = event.from_user.id
    logger.info(f"Юзер {user_id} запросил оценки.")

    if isinstance(event, CallbackQuery):
        await event.answer()
        loading_message = await event.message.edit_text("⏳ Соединяюсь с Platonus...", reply_markup=get_main_kb())
    else:
        loading_message = await event.answer("⏳ Соединяюсь с Platonus...", reply_markup=get_main_kb())
    # Важный момент: всегда отправляем актуальную клавиатуру в ответе,
    # чтобы она "закрепилась" у пользователя

    user = await User.get_or_none(telegram_id=user_id)
    if not user or not user.login or not user.password_enc:
        await loading_message.edit_text("❌ Ошибка авторизации. Нажми 'Войти'.")
        return


    try:
        grades_text, is_cached = await get_platonus_grades(user)

        if is_cached:
            grades_text += "\n\n<i>(Взято из кэша. Оценки обновляются раз в час)</i>"

        await loading_message.edit_text(grades_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Не смог спарсить оценки для {user_id}: {e}", exc_info=True)
        # Если не удалось отредактировать (например, из-за лимитов или ошибок HTML), отправляем новым сообщением
        with contextlib.suppress(BaseException):
            await loading_message.delete()
        await event.bot.send_message(chat_id=user_id, text="⚠️ Ошибка при получении оценок.", parse_mode="HTML")
