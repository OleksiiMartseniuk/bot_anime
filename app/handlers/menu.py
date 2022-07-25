from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from service.api import ApiClient
from service.service import card, ExtendedEnum


class ActionMenu(ExtendedEnum):
    """Меню"""
    anons = 'анонсы'
    filter = 'фильтр'
    search = 'поиск'


class ActionMenuFilter(ExtendedEnum):
    """Меню фильтр"""
    genre = 'отфильтровать по жанры'
    ordering = 'отсортировать'


class ActionMenuFilterOrdering(ExtendedEnum):
    """Меню Сортировки"""
    rating = 'рейтинг'
    votes = 'голоса'


class MenuStatesGroup(StatesGroup):
    """Состояния меню"""
    waiting_for_menu = State()


class FilterStatesGroup(StatesGroup):
    """Состояния меню фильтра"""
    menu_filter = State()


class FilterGenreStatesGroup(StatesGroup):
    """Состояния меню фильтра жанры"""
    menu_filter_genre = State()


class FilterOrderingStatesGroup(StatesGroup):
    """Состояния меню фильтра сортировка"""
    menu_filter_ordering = State()
    menu_filter_number = State()


async def start_menu(message: types.Message):
    """Запуск меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in ActionMenu:
        keyboard.add(name.value)
    await message.answer('Меню:', reply_markup=keyboard)
    await MenuStatesGroup.waiting_for_menu.set()


async def menu_chosen(message: types.Message, state: FSMContext):
    """Контролер меню"""
    if message.text.lower() not in ActionMenu.list():
        await message.answer(
            "Пожалуйста, выберите пункт меню, используя клавиатуру ниже.")
        return

    match message.text.lower():
        case ActionMenu.anons.value:
            await message.answer(ActionMenu.anons.value)
            await anons(message, state)
        case ActionMenu.filter.value:
            await state.finish()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for name in ActionMenuFilter:
                keyboard.add(name.value)
            await message.answer('Фильтр:', reply_markup=keyboard)
            await FilterStatesGroup.menu_filter.set()
        case ActionMenu.search.value:
            pass


async def anons(message: types.Message, state: FSMContext):
    """Вывод анонсов"""
    data = await ApiClient().get_anons()
    if data:
        for item in data['results']:
            await message.answer(
                card(item),
                reply_markup=types.ReplyKeyboardRemove(),
                parse_mode=types.ParseMode.HTML
            )
        await state.finish()
    else:
        await message.answer(
            'Что пошло не так!!!',
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()


async def menu_filter_chosen(message: types.Message, state: FSMContext):
    """Контролер меню фильтра"""
    if message.text.lower() not in ActionMenuFilter.list():
        await message.answer(
            "Пожалуйста, выберите пункт меню, используя клавиатуру ниже.")
        return

    match message.text.lower():
        case ActionMenuFilter.genre.value:
            await state.finish()
            genre_list = await ApiClient().get_genre()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for name in genre_list:
                keyboard.add(name['title'])
            await message.answer('Жанры:', reply_markup=keyboard)
            await FilterGenreStatesGroup.menu_filter_genre.set()
        case ActionMenuFilter.ordering.value:
            await state.finish()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for name in ActionMenuFilterOrdering:
                keyboard.add(name.value)
            await message.answer('Сортировка:', reply_markup=keyboard)
            await FilterOrderingStatesGroup.menu_filter_ordering.set()


async def menu_filter_genre_chosen(message: types.Message, state: FSMContext):
    """Фильтр по жанрам"""
    genre_list = await ApiClient().get_genre()
    if message.text.lower() not in [genre['title'] for genre in genre_list]:
        await message.answer(
            "Пожалуйста, выберите пункт меню, используя клавиатуру ниже.")
        return

    data = await ApiClient().get_filter_genre(message.text.lower())

    await message.answer(f'Количество: {data["count"]}')
    for item in data['results']:
        await message.answer(
            card(item),
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode=types.ParseMode.HTML
        )
    await state.finish()


async def menu_filter_ordering_chosen(
        message: types.Message,
        state: FSMContext
):
    """Сортировка"""
    if message.text.lower() not in ActionMenuFilterOrdering.list():
        await message.answer(
            "Пожалуйста, выберите пункт меню, используя клавиатуру ниже.")
        return


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(
        start_menu,
        commands="menu",
        state="*"
    )
    dp.register_message_handler(
        menu_chosen,
        state=MenuStatesGroup.waiting_for_menu
    )
    dp.register_message_handler(
        menu_filter_chosen,
        state=FilterStatesGroup.menu_filter
    )
    dp.register_message_handler(
        menu_filter_genre_chosen,
        state=FilterGenreStatesGroup.menu_filter_genre
    )
