"""
Точка входа в приложение.
Запусти этот файл командой: python main.py
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, MenuButtonCommands
from dotenv import load_dotenv

from db.database import init_db
from handlers import start, tasks

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


async def main():
    # 1. Инициализируем БД
    init_db()
    logging.info("База данных готова.")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("Токен не найден! Создай файл .env и добавь BOT_TOKEN=...")

    bot = Bot(token=token)
    dp = Dispatcher()

    # 2. Подключаем роутеры
    dp.include_router(start.router)
    dp.include_router(tasks.router)

    # 3. Регистрируем команды — появятся в меню «/» у всех пользователей
    await bot.set_my_commands([
        BotCommand(command="start",    description="Запустить бота / показать меню"),
        BotCommand(command="add",      description="Добавить задачу"),
        BotCommand(command="list",     description="Показать все задачи"),
        BotCommand(command="list_csv", description="Скачать задачи файлом CSV"),
    ])

    # 4. Показываем кнопку-меню (☰) рядом с полем ввода
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    logging.info("Бот запущен. Нажми Ctrl+C для остановки.")

    # 5. Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
