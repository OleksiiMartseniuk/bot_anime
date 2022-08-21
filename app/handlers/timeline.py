import logging

from aiogram import Dispatcher, types

from service.api import ApiClient
from service.service import card


logger = logging.getLogger(__name__)


async def start_timeline(message: types.Message):
    data = await ApiClient().get_indefinite_exit()

    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [timeline]')

    if not data:
        logger.error(f'Данные с сервера неверны запрос [get_indefinite_exit]')
        await message.answer('Что-то пошло не так!!!')
        return

    # Запись статистики
    await ApiClient().sent_statistic(
        message.from_user.id,
        'timeline',
        'Лента'
    )

    for item in data['results'][:10]:
        await message.answer_photo(
            item['url_image_preview'],
            caption=card(item),
            parse_mode=types.ParseMode.HTML
        )


def register_handlers_timeline(dp: Dispatcher):
    dp.register_message_handler(
        start_timeline,
        commands="timeline",
        state="*"
    )
