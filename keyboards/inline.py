"""
Inline-клавиатуры (кнопки внутри сообщения).
Используются для выбора категории и смены статуса задачи.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder

# Список доступных категорий и статусов
CATEGORIES = ["Разработка", "Дизайн", "Маркетинг", "Тестирование", "Общее"]
STATUSES   = ["Новая", "В работе", "Сделано", "Отменена"]

# Эмодзи для отображения статусов и категорий в тексте
STATUS_EMOJI = {
    "Новая":    "🟡",
    "В работе": "🔵",
    "Сделано":  "✅",
    "Отменена": "❌",
}

CATEGORY_EMOJI = {
    "Разработка":   "🔧",
    "Дизайн":       "🎨",
    "Маркетинг":    "📢",
    "Тестирование": "🧪",
    "Общее":        "📋",
}


def category_keyboard():
    """Клавиатура выбора категории при добавлении задачи."""
    builder = InlineKeyboardBuilder()
    for cat in CATEGORIES:
        emoji = CATEGORY_EMOJI.get(cat, "")
        # callback_data — строка, которая придёт боту при нажатии кнопки
        builder.button(text=f"{emoji} {cat}", callback_data=f"cat:{cat}")
    builder.adjust(2)  # По 2 кнопки в ряд
    return builder.as_markup()


def status_keyboard(task_id: int):
    """Клавиатура смены статуса для конкретной задачи."""
    builder = InlineKeyboardBuilder()
    for status in STATUSES:
        emoji = STATUS_EMOJI.get(status, "")
        builder.button(
            text=f"{emoji} {status}",
            callback_data=f"set_status:{task_id}:{status}",
        )
    builder.adjust(2)
    return builder.as_markup()


def task_list_keyboard(task_ids: list[int]):
    """Кнопки '✏️ #N' под списком задач для быстрой смены статуса."""
    builder = InlineKeyboardBuilder()
    for task_id in task_ids:
        builder.button(text=f"✏️ #{task_id}", callback_data=f"edit_status:{task_id}")
    builder.adjust(4)  # По 4 кнопки в ряд
    return builder.as_markup()
