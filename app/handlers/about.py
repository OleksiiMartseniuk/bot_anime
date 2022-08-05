import logging
from aiogram import Dispatcher, types

from database.db import DataBaseClient

from ..keyboards import reply


logger = logging.getLogger(__name__)


async def about_start(message: types.Message):
    """О боте"""
    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [about]')

    # Запись статистики
    await DataBaseClient().set_statistics(
        message.from_user.id,
        'about',
        'О боте'
    )

    keyboard = reply.get_about()
    await message.answer('Данный проект на этапе разработке.'
                         'Если есть какие-то вопросы, пожелания напишите нам,'
                         'ми будем очень благодарны.\n'
                         'Хорошего дня)', reply_markup=keyboard)


def register_handlers_about(dp: Dispatcher):
    dp.register_message_handler(
        about_start,
        commands="about",
        state="*"
    )

