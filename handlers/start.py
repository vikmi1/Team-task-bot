"""
Обработчик команды /start.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.reply import main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    name = message.from_user.full_name or "коллега"
    await message.answer(
        f"👋 Привет, {name}!\n\n"
        "Я помогу команде хранить общий список задач.\n\n"
        "Используй кнопки меню ниже или команды:\n"
        "/add — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — скачать задачи файлом CSV",
        reply_markup=main_menu,  # Показываем кнопки-меню
    )
