from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from parser import get_platonus_grades

router = Router()
main_keyboard= ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="🎓 Узнать оценки")]
    ],
    resize_keyboard=True
)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для проверки оценок в Платонусе. Отправь /grades, чтобы узнать свои оценки.",
    reply_markup=main_keyboard
    )   

@router.message(Command("grades"))
@router.message(F.text == "🎓 Узнать оценки")
async def cmd_grades(message: Message):
    loading_message = await message.answer("⏳ Получаю твои оценки...")
    grades_text = await get_platonus_grades()
    await loading_message.edit_text(grades_text, parse_mode="HTML")