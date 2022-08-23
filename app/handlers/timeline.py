import logging

from aiogram import Dispatcher, types

from service.api import ApiClient
from service.service import card, get_image


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
        img = get_image(item['url_image_preview'], item['telegram_id_file'])
        await message.answer_photo(
            img,
            caption=card(item),
            parse_mode=types.ParseMode.HTML
        )


def register_handlers_timeline(dp: Dispatcher):
    dp.register_message_handler(
        start_timeline,
        commands="timeline",
        state="*"
    )
