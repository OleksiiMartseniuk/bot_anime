import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from service.api import ApiClient
from service.service import user_registration


logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "<b>Выберите действия</b>\n"
        "/profile - Профиль\n"
        "/schedules - расписания\n"
        "/timeline - лента\n"
        "/anons - анонс\n"
        "/search - поиск\n"
        "/filter_genre - фильтр по жанрам\n"
        "/about - о нас\n",
        parse_mode=types.ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )
    # Регистрация пользователя
    await user_registration(
        message.from_user.username,
        message.from_user.id,
        message.chat.id
    )
    # Запись статистики
    await ApiClient().sent_statistic(
        message.from_user.id,
        'start',
        'Начало роботы'
    )
    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [start]')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Действие отменено",
        reply_markup=types.ReplyKeyboardRemove()
    )
    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [cancel]')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel,
        Text(equals="отмена", ignore_case=True),
        state="*"
    )
