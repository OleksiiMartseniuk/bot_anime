from aiogram.types import ReplyKeyboardMarkup

from service.service import Week


available_anime = ['текущий день'] + [day.value for day in Week]


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


def get_schedules() -> ReplyKeyboardMarkup:
    """Расписания"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_anime:
        keyboard.add(name.capitalize())
    return keyboard


def get_about() -> ReplyKeyboardMarkup:
    """О боте"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Отправить сообщения')
    keyboard.add('Отмена')
    return keyboard
