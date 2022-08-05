import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from database.db import DataBaseClient

from service.api import ApiClient
from service.service import card, get_page_list

from ..states.search import SearchName
from ..keyboards import reply


logger = logging.getLogger(__name__)


async def search_start(message: types.Message):
    """Получения поискового запроса"""
    await message.answer('Введите названия....✍️')
    await SearchName.waiting_for_name.set()


async def result_search(message: types.Message, state: FSMContext):
    """Результат поиска"""
    data = await ApiClient().search(message.text.lower())

    logger.info(f'Пользователь [{message.from_user.id}]  '
                f'задал поиск [{message.text.lower()}]')

    if not data:
        await message.answer('Что-то пошло не так!!!')
        logger.error(f'Данные с сервера неверны запрос '
                     f'[search({message.text.lower()})]')
        await state.finish()
        return

    # Запись статистики
    await DataBaseClient().set_statistics(
        message.from_user.id,
        'search',
        f'Поиск по [{message.text.lower()}]'
    )

    if data['count'] == 0:
        await message.answer('Нечего не найдено...')
        await state.finish()
        return

    await message.answer(
        f"<b>Найдено</b>: \t {data['count']} аниме",
        parse_mode=types.ParseMode.HTML,
    )

    page_list = get_page_list(data['count'])
    search = message.text.lower()
    await state.update_data(page_list=page_list, search=search)
    await SearchName.next()

    keyboard = reply.get_pagination()
    await message.answer('Выберете действия:', reply_markup=keyboard)


async def pagination_search(message: types.Message, state: FSMContext):
    """Пагинация по страницам"""
    if message.text.lower() == 'показать страницу':
        user_data = await state.get_data()

        if user_data['page_list']:
            data = await ApiClient().search(
                user_data['search'],
                user_data['page_list'][-1]
            )
            for item in data['results']:
                await message.answer_photo(
                    item['url_image_preview_s'],
                    caption=card(item),
                    parse_mode=types.ParseMode.HTML
                )

            user_data['page_list'].pop()
            if not user_data['page_list']:
                await message.answer(
                    '🔚',
                    reply_markup=types.ReplyKeyboardRemove()
                )
                await state.finish()
                return
            await state.update_data(page_list=user_data['page_list'])


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
    dp.register_message_handler(
        pagination_search,
        state=SearchName.waiting_for_page
    )
