"""
Обработчики для работы с задачами:
  /add, «➕ Добавить задачу» — пошаговое добавление через FSM
  /list, «📋 Список задач»   — список всех задач с кнопками смены статуса
  «📂 По категориям»          — задачи, сгруппированные по категориям
  /list_csv, «📥 Скачать CSV» — экспорт в файл
  Callback-обработчики для смены статуса задачи
"""

import csv
import io

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from db.database import add_task, get_all_tasks, get_task_by_id, update_task_status
from handlers.states import AddTask
from keyboards.inline import (
    CATEGORY_EMOJI,
    STATUS_EMOJI,
    category_keyboard,
    status_keyboard,
    task_list_keyboard,
)

router = Router()


# ─── Добавление задачи (FSM) ──────────────────────────────────────────────────

# Оба триггера: slash-команда и кнопка меню — запускают один обработчик
@router.message(Command("add"))
@router.message(F.text == "➕ Добавить задачу")
async def cmd_add(message: Message, state: FSMContext):
    """Шаг 1: переходим в состояние ожидания текста задачи."""
    await state.set_state(AddTask.waiting_for_text)
    await message.answer("✏️ Введите текст задачи:")


@router.message(AddTask.waiting_for_text)
async def process_task_text(message: Message, state: FSMContext):
    """Шаг 2: текст получен — сохраняем в FSM и просим выбрать категорию."""
    # state.update_data сохраняет данные между шагами FSM
    await state.update_data(task_text=message.text.strip())
    await state.set_state(AddTask.waiting_for_category)
    await message.answer("📂 Выберите категорию:", reply_markup=category_keyboard())


@router.callback_query(F.data.startswith("cat:"), AddTask.waiting_for_category)
async def process_category(callback: CallbackQuery, state: FSMContext):
    """Шаг 3: категория выбрана — сохраняем задачу в базу данных."""
    category = callback.data.split(":", 1)[1]
    data = await state.get_data()
    task_text = data["task_text"]
    user = callback.from_user.full_name or callback.from_user.username or "Аноним"

    task_id = add_task(task_text, user, category)
    await state.clear()  # Сбрасываем состояние FSM

    emoji = CATEGORY_EMOJI.get(category, "📋")
    # Редактируем сообщение с клавиатурой категорий — заменяем на результат
    await callback.message.edit_text(
        f"✅ Задача #{task_id} добавлена!\n\n"
        f"📝 {task_text}\n"
        f"{emoji} Категория: {category}\n"
        f"🟡 Статус: Новая"
    )
    await callback.answer("Задача сохранена!")


# ─── Список задач ─────────────────────────────────────────────────────────────

@router.message(Command("list"))
@router.message(F.text == "📋 Список задач")
async def cmd_list(message: Message):
    """Показывает все задачи. Под списком — кнопки для смены статуса."""
    tasks = get_all_tasks()
    if not tasks:
        await message.answer("📭 Список пуст. Нажмите «➕ Добавить задачу».")
        return

    lines = ["📋 <b>Все задачи:</b>\n"]
    task_ids = []

    for task_id, text, user, created_at, category, status in tasks:
        s_emoji = STATUS_EMOJI.get(status, "❓")
        c_emoji = CATEGORY_EMOJI.get(category, "📋")
        lines.append(
            f"{s_emoji} <b>#{task_id}</b> {c_emoji} <i>{category}</i>\n"
            f"   {text}\n"
            f"   👤 {user} · {created_at}\n"
        )
        task_ids.append(task_id)

    lines.append("<i>Нажмите ✏️ #N чтобы изменить статус задачи</i>")

    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=task_list_keyboard(task_ids),
    )


# ─── Список по категориям ─────────────────────────────────────────────────────

@router.message(F.text == "📂 По категориям")
async def cmd_list_by_category(message: Message):
    """Показывает задачи, сгруппированные по категориям."""
    tasks = get_all_tasks()
    if not tasks:
        await message.answer("📭 Список пуст. Нажмите «➕ Добавить задачу».")
        return

    # Группируем задачи по полю category
    grouped: dict[str, list] = {}
    for row in tasks:
        category = row[4]
        grouped.setdefault(category, []).append(row)

    lines = ["📂 <b>Задачи по категориям:</b>\n"]
    for category, cat_tasks in grouped.items():
        c_emoji = CATEGORY_EMOJI.get(category, "📋")
        lines.append(f"{c_emoji} <b>{category}</b> ({len(cat_tasks)}):")
        for task_id, text, user, _, _, status in cat_tasks:
            s_emoji = STATUS_EMOJI.get(status, "❓")
            lines.append(f"  {s_emoji} #{task_id} {text} — {user}")
        lines.append("")

    await message.answer("\n".join(lines), parse_mode="HTML")


# ─── Смена статуса (callback) ─────────────────────────────────────────────────

@router.callback_query(F.data.startswith("edit_status:"))
async def ask_new_status(callback: CallbackQuery):
    """Пользователь нажал ✏️ #N — показываем клавиатуру выбора статуса."""
    task_id = int(callback.data.split(":")[1])
    task = get_task_by_id(task_id)

    if not task:
        await callback.answer("Задача не найдена.", show_alert=True)
        return

    _, text, _, _, _, status = task
    s_emoji = STATUS_EMOJI.get(status, "❓")

    await callback.message.answer(
        f"📝 <b>Задача #{task_id}:</b> {text}\n"
        f"Текущий статус: {s_emoji} {status}\n\n"
        "Выберите новый статус:",
        parse_mode="HTML",
        reply_markup=status_keyboard(task_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_status:"))
async def set_task_status(callback: CallbackQuery):
    """Пользователь выбрал статус — обновляем в базе данных."""
    # Формат callback_data: "set_status:{task_id}:{status}"
    parts = callback.data.split(":", 2)
    task_id = int(parts[1])
    new_status = parts[2]

    update_task_status(task_id, new_status)

    s_emoji = STATUS_EMOJI.get(new_status, "❓")
    # Редактируем сообщение с клавиатурой — заменяем на результат
    await callback.message.edit_text(
        f"{s_emoji} Задача #{task_id}: статус изменён на «{new_status}»"
    )
    await callback.answer(f"Готово: {new_status}")


# ─── Экспорт CSV ──────────────────────────────────────────────────────────────

@router.message(Command("list_csv"))
@router.message(F.text == "📥 Скачать CSV")
async def cmd_list_csv(message: Message):
    """Отправляет все задачи файлом tasks.csv."""
    tasks = get_all_tasks()
    if not tasks:
        await message.answer("📭 Список пуст, CSV не создан.")
        return

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Задача", "Пользователь", "Дата создания", "Категория", "Статус"])
    for row in tasks:
        writer.writerow(row)

    # utf-8-sig — кодировка с BOM, чтобы Excel правильно открыл кириллицу
    csv_bytes = output.getvalue().encode("utf-8-sig")
    file = BufferedInputFile(csv_bytes, filename="tasks.csv")
    await message.answer_document(file, caption=f"📊 Задач в списке: {len(tasks)}")
