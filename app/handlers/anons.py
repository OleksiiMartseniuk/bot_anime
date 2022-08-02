import logging
from aiogram import Dispatcher, types

from database.db import DataBaseClient

from service.api import ApiClient
from service.service import card


logger = logging.getLogger(__name__)


async def anons_start(message: types.Message):
    """Получения анонсов"""
    data = await ApiClient().get_anons()

    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [анонс]')

    if not data:
        logger.error(f'Данные с сервера неверны запрос [get_anons]')
        await message.answer('Что-то пошло не так!!!')
        return

    # Запись статистики
    await DataBaseClient().set_statistics(
        message.from_user.id,
        'anons',
        'Получения анонсов'
    )

    await message.answer(
        f"<b>Анонс</b> \n"
        f"<b>Количество</b>: \t {data['count']}",
        parse_mode=types.ParseMode.HTML
    )
    for item in data['results']:
        await message.answer_photo(
            item['url_image_preview'],
            caption=card(item),
            parse_mode=types.ParseMode.HTML
        )


def register_handlers_anons(dp: Dispatcher):
    dp.register_message_handler(
        anons_start,
        commands="anons",
        state="*"
    )
