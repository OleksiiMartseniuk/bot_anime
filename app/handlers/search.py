import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from service.api import ApiClient
from service.service import card
from ..states.search import SearchName


logger = logging.getLogger(__name__)


async def search_start(message: types.Message):
    """Получения поискового запроса"""
    await message.answer('Введите названия....✍️')
    await SearchName.waiting_for_name.set()


async def result_search(message: types.Message, state: FSMContext):
    data = await ApiClient().search(message.text.lower())

    logger.info(f'Пользователь [{message.from_user.id}]  '
                f'задал поиск [{message.text.lower()}]')

    if not data:
        await message.answer('Что-то пошло не так!!!')
        logger.error(f'Данные с сервера неверны запрос '
                     f'[search({message.text.lower()})]')
        return

    if data['count'] == 0:
        await message.answer('Нечего не найдено...')
        await state.finish()
        return

    await message.answer(
        f"<b>Найдено</b>: \t {data['count']} аниме",
        parse_mode=types.ParseMode.HTML,
    )
    for item in data['results']:
        await message.answer_photo(
            item['url_image_preview'],
            caption=card(item),
            parse_mode=types.ParseMode.HTML
        )
    await state.finish()


def register_handlers_search(dp: Dispatcher):
    dp.register_message_handler(
        search_start,
        commands="search",
        state="*"
    )
    dp.register_message_handler(
        result_search,
        state=SearchName.waiting_for_name
    )
    