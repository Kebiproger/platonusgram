from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from parser import get_platonus_grades
from db_api import get_user, save_user
from crypto import decrypt_password, js_decrypt_password, fernet_encrypt_password
from keyboards import get_main_kb, get_login_kb
import json

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Проверяем, есть ли юзер в БД
    user = get_user(message.from_user.id)
    
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
    
    # 1. Достаем ту самую JSON-строку, которую мы отправили из JS
    raw_data = message.web_app_data.data
    
    # 2. Превращаем строку в словарь Python
    parsed_data = json.loads(raw_data)
    
    if parsed_data.get("action") == "login":
        encrypted_pass = parsed_data.get("password")
        platonus_login = parsed_data.get("login")
        if not platonus_login or not encrypted_pass:
            await message.answer("❌ Ошибка: Данные неполные. Пожалуйста, очистите кэш Телеграма и попробуйте снова.")
            return
        # 4. Расшифровываем!
        real_password = js_decrypt_password(encrypted_pass)
        save_user(message.from_user.id, platonus_login, fernet_encrypt_password(real_password))
        
        # 5. Отвечаем юзеру
        await message.answer("Пароль успешно получен и зашифрован!Если хочешь узнать оценки, нажми '🎓 Узнать оценки',если хочешь повторно логиниться то нажми команду /login", reply_markup=get_main_kb())

@router.message(Command("login"))
async def login_cmd(message: Message):
    login_kb = get_login_kb()
    await message.answer("Нажми на кнопку ниже, чтобы безопасно ввести пароль:", reply_markup=login_kb)

@router.message(Command("grades"))
@router.callback_query(F.data == "grades")
async def cmd_grades(callback: CallbackQuery):
    await callback.answer()
    # Важный момент: всегда отправляем актуальную клавиатуру в ответе, 
    # чтобы она "закрепилась" у пользователя
    loading_message = await callback.message.edit_text("⏳ Соединяюсь с Platonus...", reply_markup=get_main_kb())
    
    row = get_user(callback.from_user.id)
    if not row:
        await loading_message.edit_text("❌ Ошибка авторизации. Нажми 'Войти'.", reply_markup=get_login_kb())
        return

    # Твоя логика получения оценок...
    username, password_enc = row
    password = decrypt_password(password_enc)
    
    grades_text = await get_platonus_grades(username, password)
    try:
        await loading_message.edit_text(grades_text, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Не удалось отредактировать сообщение: {e}")
        # Если не удалось отредактировать (например, из-за лимитов или ошибок HTML), отправляем новым сообщением
        await callback.message.answer(grades_text, parse_mode="HTML")
