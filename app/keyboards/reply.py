from aiogram.types import ReplyKeyboardMarkup


def get_genre(genre_list: list) -> ReplyKeyboardMarkup:
    """Жанры"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in genre_list:
        keyboard.add(item['title'])
    return keyboard


def get_pagination() -> ReplyKeyboardMarkup:
    """Кнопки пагинации"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Показать страницу')
    keyboard.add('Отмена')
    return keyboard
