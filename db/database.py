"""
Модуль для работы с базой данных SQLite.
Таблица tasks теперь хранит также категорию и статус задачи.
"""

import sqlite3
from datetime import datetime

DB_PATH = "tasks.db"


def init_db():
    """Создаёт таблицу tasks и добавляет новые колонки в существующую БД."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            text       TEXT    NOT NULL,
            user       TEXT    NOT NULL,
            created_at TEXT    NOT NULL,
            category   TEXT    NOT NULL DEFAULT 'Общее',
            status     TEXT    NOT NULL DEFAULT 'Новая'
        )
    """)

    # Миграция: добавляем колонки если их ещё нет (для старых баз данных)
    for col, definition in [
        ("category", "TEXT NOT NULL DEFAULT 'Общее'"),
        ("status",   "TEXT NOT NULL DEFAULT 'Новая'"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE tasks ADD COLUMN {col} {definition}")
        except sqlite3.OperationalError:
            pass  # Колонка уже существует — пропускаем

    conn.commit()
    conn.close()


def add_task(text: str, user: str, category: str = "Общее") -> int:
    """Добавляет задачу и возвращает её ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "INSERT INTO tasks (text, user, created_at, category, status) VALUES (?, ?, ?, ?, ?)",
        (text, user, created_at, category, "Новая"),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_all_tasks() -> list[tuple]:
    """Возвращает все задачи: (id, text, user, created_at, category, status)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, text, user, created_at, category, status FROM tasks ORDER BY id"
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def get_task_by_id(task_id: int) -> tuple | None:
    """Возвращает одну задачу по ID или None если не найдена."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, text, user, created_at, category, status FROM tasks WHERE id = ?",
        (task_id,),
    )
    task = cursor.fetchone()
    conn.close()
    return task


def update_task_status(task_id: int, new_status: str):
    """Обновляет статус задачи."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()
