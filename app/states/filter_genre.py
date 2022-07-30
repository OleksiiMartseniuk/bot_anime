from aiogram.dispatcher.filters.state import State, StatesGroup


class FilterGenre(StatesGroup):
    """Состояния для выбора жанра"""
    waiting_for_genre = State()
    waiting_for_page = State()
