import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from datetime import datetime

from service.api import ApiClient
from service.service import card, Week
from ..states.schedules import WeekDay

logger = logging.getLogger(__name__)

available_anime = ['текущий день'] + [day.value for day in Week]


async def anime_start(message: types.Message):
    """Выбор действия"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_anime:
        keyboard.add(name)
    await message.answer('Выберите день:', reply_markup=keyboard)
    await WeekDay.waiting_for_day.set()


async def anime_chosen(message: types.Message, state: FSMContext):
    """Вывод расписания"""
    if message.text.lower() not in available_anime:
        await message.answer(
            "Пожалуйста, выберите действия, используя клавиатуру ниже."
        )
        return

    logger.info(f'Пользователь [{message.from_user.id}]  '
                f'выбрал действия [{message.text.lower()}]')

    if message.text.lower() == available_anime[0]:
        day = list(Week)[datetime.weekday(datetime.now())]
        data = await ApiClient().get_anime_day(day.name)
    else:
        for day_week in Week:
            if day_week.value == message.text.lower():
                data = await ApiClient().get_anime_day(day_week.name)
                day = day_week

    if not data:
        logger.error(f'Данные с сервера неверны запрос '
                     f'get_anime_day[{day.name}]')
        await message.answer('Что-то пошло не так!!!')
        return

    await message.answer(f"{day.value}\n"
                         f"количество: {data['count']} аниме")
    for item in data['results']:
        await message.answer_photo(
            item['url_image_preview'],
            caption=card(item, schedules=True),
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode=types.ParseMode.HTML
        )
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
        state=WeekDay.waiting_for_day
    )
