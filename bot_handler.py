from aiogram import Router, F, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from parser import get_platonus_grades
from config import URL
import secrets
from web_server import active_tokens
from db_api import get_user
from crypto import decrypt_password

router = Router()
main_keyboard= ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="🎓 Узнать оценки")]
    ],
    resize_keyboard=True
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🔑 Войти")]],
    resize_keyboard=True
)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer('''👋 Привет! Я — твой независимый ассистент для учебы.

Я избавлю тебя от необходимости постоянно проверять портал. Я буду сам следить за твоим журналом и расписанием, а ты сможешь сфокусироваться на главном.

⚠️ Проект создан студентами для студентов и не является официальным ботом университета.

Чтобы начать получать уведомления об оценках, нажми кнопку ниже и авторизуйся в системе (это нужно сделать всего один раз):''',
    reply_markup=start_keyboard
    )   

@router.message(Command("login"))
@router.message(F.text == "🔑 Войти")
async def cmd_login(message: types.Message):
    # 1. ГЕНЕРАЦИЯ: Вызываем твою функцию и передаем ей ID пользователя.
    # Она возвращает готовую ссылку: http://твой_ip/login?token=a1b2...
    login_url = create_login_link(message.from_user.id)
    
    # 2. УПАКОВКА: Создаем красивую кнопку (Inline-кнопка под сообщением)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🔑 Войти в Platonus", 
        url=login_url  # Вшиваем нашу сгенерированную ссылку в кнопку!
    ))
    
    # 3. ОТПРАВКА: Бот отправляет текст и прикрепляет к нему кнопку
    await message.answer(
        "Нажмите на кнопку ниже, чтобы безопасно ввести пароль.\n"
        "Ссылка одноразовая и сгорит после использования!",
        reply_markup=builder.as_markup()
    )

@router.message(Command("grades"))
@router.message(F.text == "🎓 Узнать оценки")
async def cmd_grades(message: Message):
    
    loading_message = await message.answer("⏳ Получаю твои оценки...")
    row = get_user(message.from_user.id)
    
    if not row:
        await loading_message.edit_text("❌ Вы не авторизованы! Наберите /login и перейдите по ссылке.")
        return
        
    username, password_enc = row
    password = decrypt_password(password_enc)
    print(f"DEBUG: auth grades for {username}, password dec: {bool(password)}")
    
    grades_text = await get_platonus_grades(username, password)
    await loading_message.edit_text(grades_text, parse_mode="HTML")

def create_login_link(telegram_id: int) -> str:
    token = secrets.token_urlsafe(32)
    active_tokens[token] = telegram_id
    return f"{URL}/login?token={token}"