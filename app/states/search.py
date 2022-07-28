from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchName(StatesGroup):
    """Состояния для поиска"""
    waiting_for_name = State()
