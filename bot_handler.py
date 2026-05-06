from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser import get_platonus_grades
from db_api import get_user
from crypto import decrypt_password 
from web_server import active_tokens
import secrets
from config import URL
from keyboards import get_main_kb, get_start_kb

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
        kb = get_start_kb()

    await message.answer(text, reply_markup=kb)

@router.message(Command("login"))
@router.message(F.text == "🔑 Войти")
async def cmd_login(message: Message):
    login_url = create_login_link(message.from_user.id)
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔑 Перейти к авторизации", url=login_url))
    
    await message.answer(
        "Безопасный вход: ссылка откроется в браузере и сгорит после ввода пароля.",
        reply_markup=builder.as_markup()
    )

@router.message(F.text == "🎓 Узнать оценки")
async def cmd_grades(message: Message):
    # Важный момент: всегда отправляем актуальную клавиатуру в ответе, 
    # чтобы она "закрепилась" у пользователя
    loading_message = await message.answer("⏳ Соединяюсь с Platonus...", reply_markup=get_main_kb())
    
    row = get_user(message.from_user.id)
    if not row:
        await loading_message.edit_text("❌ Ошибка авторизации. Нажми 'Войти'.", reply_markup=get_start_kb())
        return

    # Твоя логика получения оценок...
    username, password_enc = row
    password = decrypt_password(password_enc)
    
    grades_text = await get_platonus_grades(username, password)
    await loading_message.edit_text(grades_text, parse_mode="HTML")

def create_login_link(telegram_id: int) -> str:

    token = secrets.token_urlsafe(32)

    active_tokens[token] = telegram_id

    return f"{URL}/login?token={token}" 