from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_kb():
    """Клавиатура для авторизованного пользователя"""
    return InlineKeyboardMarkup(
        keyboard=[[InlineKeyboardButton(text="🎓 Узнать оценки", callback_data="grades")]],
        resize_keyboard=True,
        persistent=True  # Кнопка не будет прятаться под иконку
    )

def get_login_kb():
    web_app_btn = KeyboardButton(
        text="🔑 Ввести пароль",
        web_app=WebAppInfo(url="https://kebiproger.github.io/platonus.iitu.edu.kz/?v=2")
    )
    return ReplyKeyboardMarkup(keyboard=[[web_app_btn]], resize_keyboard=True)
