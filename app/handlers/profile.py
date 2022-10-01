import logging

from aiogram import Dispatcher, types

from service.api import ApiClient
from service.service import card

from ..keyboards.inline import menu_profile


logger = logging.getLogger(__name__)


async def profile_menu(message: types.Message):
    """Меню"""
    await list_categories(message)


async def list_categories(
    message: types.Message | types.CallbackQuery, *args, **kwargs
):
    """Список категорий"""
    markup = await menu_profile.categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer('Профиль', reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        callback = message
        await callback.message.edit_reply_markup(markup)


async def list_anime(callback: types.CallbackQuery, category, **kwargs):
    markup = await menu_profile.list_anime_keyboard(
        category, callback.from_user.id
    )
    """Список anime"""
    await callback.message.edit_text('Выбрать из списка', reply_markup=markup)


async def show_anime(
    callback: types.CallbackQuery, category, item_id, **kwargs
):
    """Вывод аниме"""
    markup = menu_profile.item_keyboard(item_id, category)
    anime = await ApiClient().get_anime(int(item_id))
    await callback.message.edit_text(
        card(anime, schedules=True),
        reply_markup=markup,
        parse_mode=types.ParseMode.HTML
    )


async def navigate(call: types.CallbackQuery, callback_data: dict):
    """Навигация меню"""
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    item_id = callback_data.get('item_id')

    levels = {
        '0': list_categories,
        '1': list_anime,
        '2': show_anime
    }
    current_level_function = levels[current_level]
    await current_level_function(call, category=category, item_id=item_id)


async def subscribe(call: types.CallbackQuery, callback_data: dict):
    """Кнопка подписки"""
    category = callback_data.get('category')
    item_id = callback_data.get('item_id')
    level = callback_data.get('level')

    markup = await menu_profile.set_subscribe(
        level, item_id, category, call.from_user.id
    )

    text = '✅ Выполнено' if markup else '❗️ Что-то пошло не так.\n'\
        'Возможно вы не зарегистрированы используйте /start'
    await call.message.edit_text(text, reply_markup=markup)


def register_handlers_profile(dp: Dispatcher):
    dp.register_message_handler(
        profile_menu,
        commands="profile",
        state="*"
    )
    dp.register_callback_query_handler(
        navigate,
        menu_profile.menu_cd.filter()
    )
    dp.register_callback_query_handler(
        subscribe,
        menu_profile.buy_item.filter()
    )
