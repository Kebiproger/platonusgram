from aiogram.types import (
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import hashlib

def get_main_kb() -> ReplyKeyboardMarkup:
    """
    Создает нижнее Главное меню.
    """
    builder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки по одной
    builder.button(text="📊 Мои оценки")
    builder.button(text="📅 Расписание")
    # builder.button(text="⚙️ Настройки", callback_data="settings")

    # Метод adjust() автоматически выстраивает кнопки по рядам!
    # (2, 1) означает: 2 кнопки в первом ряду, 1 во втором.
    builder.adjust(2, 1)
    
    # resize_keyboard=True делает кнопки аккуратными (не на пол-экрана)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выбери действие...")


def get_grades_inline_kb() -> InlineKeyboardMarkup:
    """
    Создает инлайн-кнопку "Обновить" под сообщением с оценками.
    """
    builder = InlineKeyboardBuilder()
    
    # callback_data - это то, что перехватит твой @router.callback_query()
    builder.button(text="🔄 Обновить оценки", callback_data="grades")
    
    return builder.as_markup()

def get_subjects_kb(grades_dict: dict) -> InlineKeyboardMarkup:
    """Генерирует кнопки с названиями предметов"""
    builder = InlineKeyboardBuilder()
    
    for index, subject_name in enumerate(grades_dict.keys(), start=1):
        # Хэш все равно нужен, чтобы хэндлер понял, какой именно предмет открывать
        short_id = hashlib.md5(subject_name.encode()).hexdigest()[:10]
        
        # На кнопке пишем только номер! Например: "1" или "2"
        builder.button(text=f"{index}", callback_data=f"subj_{short_id}")
        
    # Добавляем общую кнопку обновления в самый низ
    builder.button(text="🔄 Обновить все", callback_data="grades")
    buttons_count = len(grades_dict)
    builder.adjust(4, buttons_count % 4, 1)
    return builder.as_markup()

def get_back_to_subjects_kb() -> InlineKeyboardMarkup:
    """Кнопка возврата к списку"""
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад к списку", callback_data="back_to_subjects")
    return builder.as_markup()

def get_login_kb():
    web_app_btn = KeyboardButton(
        text="🔑 Ввести пароль",
        web_app=WebAppInfo(url="https://kebiproger.github.io/platonus.iitu.edu.kz/?v=2")
    )
    return ReplyKeyboardMarkup(keyboard=[[web_app_btn]], resize_keyboard=True)
