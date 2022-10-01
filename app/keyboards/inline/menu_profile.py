import logging
from dataclasses import dataclass

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from service.api import ApiClient


logger = logging.getLogger(__name__)


@dataclass
class MenuProfile:
    title: str
    action: str


menu_list = [
    MenuProfile(title='Список подписок', action=1),
    MenuProfile(title='Список доступных для подписки', action=0),
]

menu_cd = CallbackData('profile_menu', 'level', 'category', 'item_id')
buy_item = CallbackData('buy', 'item_id', 'category', 'level')


def make_callback_data(level, category='0', item_id='0') -> CallbackData:
    """Сбор callback_data"""
    return menu_cd.new(level=level, category=category, item_id=item_id)


async def categories_keyboard() -> types.InlineKeyboardMarkup:
    """Вывод категорий"""
    CURRENT_LEVEL = 0

    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in menu_list:
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=item.action
        )
        markup.insert(
            types.InlineKeyboardButton(
                text=item.title, callback_data=callback_data
            )
        )
    return markup


async def list_anime_keyboard(
    category, user_id
) -> types.InlineKeyboardMarkup:
    """Список anime"""
    CURRENT_LEVEL = 1

    markup = types.InlineKeyboardMarkup(row_width=1)
    data = await ApiClient().get_anime_track(int(user_id), bool(int(category)))

    if data:
        for anime in data:
            try:
                button_text = anime['title'].split('/')[0]
            except IndexError:
                button_text = anime['title']

            callback_data = make_callback_data(
                level=CURRENT_LEVEL + 1, item_id=anime['id'], category=category
            )
            markup.insert(
                types.InlineKeyboardButton(
                    text=button_text, callback_data=callback_data
                )
            )
    markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


def item_keyboard(item_id, category):
    """Вывод аниме"""
    CURRENT_LEVEL = 2

    text = 'Отменить подписку' if bool(int(category)) else 'Подписаться'
    markup = types.InlineKeyboardMarkup()
    markup.row(
            types.InlineKeyboardButton(
                text=text, callback_data=buy_item.new(
                    item_id=item_id, category=category, level=CURRENT_LEVEL
                )
            )
        )
    markup.row(
        types.InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category
            )
        )
    )
    return markup


async def set_subscribe(level, item_id, category, user_id):
    """Подписка"""
    if bool(int(category)):
        response = await ApiClient().remove_anime_track(
            [int(item_id)], user_id
        )
    else:
        response = await ApiClient().add_anime_track([int(item_id)], user_id)

    if not response:
        logger.error(f'set_subscribe Пользователь[{user_id}] anime[{item_id}]')
        return

    return await categories_keyboard()
