from aiogram.dispatcher.filters.state import State, StatesGroup


class AboutMessage(StatesGroup):
    """Состояния для написания сообщения"""
    waiting_for_star_about = State()
    waiting_for_write_massage = State()
