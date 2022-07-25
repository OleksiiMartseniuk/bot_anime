from enum import Enum

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from service.api import ApiClient
from service.service import card


class ActionMenu(Enum):
    """Меню"""
    anons = 'анонсы'
    filter = 'фильтр'
    search = 'поиск'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ActionMenu))


class MenuStatesGroup(StatesGroup):
    """Состояния меню"""
    waiting_for_menu = State()


async def start_menu(message: types.Message):
    """Запуск меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in ActionMenu:
        keyboard.add(name.value)
    await message.answer('Меню:', reply_markup=keyboard)
    await MenuStatesGroup.waiting_for_menu.set()


async def menu_chosen(message: types.Message, state: FSMContext):
    """"""
    if message.text.lower() not in ActionMenu.list():
        await message.answer(
            "Пожалуйста, выберите пункт меню, используя клавиатуру ниже.")
        return

    match message.text.lower():
        case ActionMenu.anons.value:
            await message.answer(ActionMenu.anons.value)
            await anons(message, state)
        case ActionMenu.filter.value:
            pass
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
