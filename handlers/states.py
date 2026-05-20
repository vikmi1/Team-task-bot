"""
FSM-состояния (Finite State Machine) — шаги при добавлении задачи.
Бот «запоминает», на каком шаге находится пользователь.
"""

from aiogram.fsm.state import State, StatesGroup


class AddTask(StatesGroup):
    waiting_for_text = State()      # Шаг 1: ждём текст задачи
    waiting_for_category = State()  # Шаг 2: ждём выбор категории
