from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb():
    """Клавиатура для авторизованного пользователя"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🎓 Узнать оценки")]],
        resize_keyboard=True,
        persistent=True  # Кнопка не будет прятаться под иконку
    )

def get_start_kb():
    """Клавиатура для новичка"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔑 Войти")]],
        resize_keyboard=True
    )
