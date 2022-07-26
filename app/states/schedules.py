from aiogram.dispatcher.filters.state import State, StatesGroup


class WeekDay(StatesGroup):
    """Состояния для выбора дня недели"""
    waiting_for_day = State()
