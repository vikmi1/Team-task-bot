"""
Reply-клавиатура — кнопки под полем ввода.
Появляется после /start и остаётся постоянно.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        # Первый ряд кнопок
        [
            KeyboardButton(text="➕ Добавить задачу"),
            KeyboardButton(text="📋 Список задач"),
        ],
        # Второй ряд кнопок
        [
            KeyboardButton(text="📂 По категориям"),
            KeyboardButton(text="📥 Скачать CSV"),
        ],
    ],
    resize_keyboard=True,                            # Кнопки нормального размера
    input_field_placeholder="Выберите действие...",  # Подсказка в поле ввода
)
