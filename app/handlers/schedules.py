from enum import Enum

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from datetime import datetime

from service.api import ApiClient
from service.service import card


class Week(Enum):
    monday = 'понедельник'
    tuesday = 'вторник'
    wednesday = 'среда'
    thursday = 'четверг'
    friday = 'пятница'
    saturday = 'суббота'
    sunday = 'воскресенье'


available_anime = ['текущий день'] + [day.value for day in Week]


class SchedulesAnime(StatesGroup):
    """Состояния"""
    waiting_for_day = State()


async def anime_start(message: types.Message):
    """Выбор действия"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_anime:
        keyboard.add(name)
    await message.answer('Выберите день:', reply_markup=keyboard)
    await SchedulesAnime.waiting_for_day.set()


async def anime_chosen(message: types.Message, state: FSMContext):
    """Вывод расписания"""
    if message.text.lower() not in available_anime:
        await message.answer(
            "Пожалуйста, выберите действия, используя клавиатуру ниже."
        )
        return

    if message.text.lower() == available_anime[0]:
        day = list(Week)[datetime.weekday(datetime.now())]
        data = await ApiClient().get_anime_day(day.name)
    else:
        for day_week in Week:
            if day_week.value == message.text.lower():
                data = await ApiClient().get_anime_day(day_week.name)
                day = day_week

    await message.answer(day.value)
    if data:
        for item in data['results']:
            await message.answer(
                card(item, schedules=True),
                reply_markup=types.ReplyKeyboardRemove(),
                parse_mode=types.ParseMode.HTML
            )
    else:
        await message.answer('Что-то пошло не так!!!')
    # Сбросит состояние и хранящиеся данные
    await state.finish()


def register_handlers_schedules(dp: Dispatcher):
    dp.register_message_handler(
        anime_start,
        commands="anime_schedules",
        state="*"
    )
    dp.register_message_handler(
        anime_chosen,
        state=SchedulesAnime.waiting_for_day
    )
