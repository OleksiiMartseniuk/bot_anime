import logging
import math

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from service.api import ApiClient
from service.service import card

from ..states.filter_genre import FilterGenre


logger = logging.getLogger(__name__)


async def filter_genre_start(message: types.Message):
    """Вывод жанров"""
    data = await ApiClient().get_genre()

    if not data:
        await message.answer(
            'Что-то пошло не так!!!',
            reply_markup=types.ReplyKeyboardRemove()
        )
        logger.error(f'Данные с сервера неверны запрос [get_genre]')
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data:
        keyboard.add(item['title'])
    await message.answer('Выберите жанр:', reply_markup=keyboard)
    await FilterGenre.waiting_for_genre.set()


async def filter_genre_result(message: types.Message, state: FSMContext):
    """Получения результата фильтра"""
    data_genre = await ApiClient().get_genre()
    if message.text.lower() not in [item['title'] for item in data_genre]:
        await message.answer(
            "Пожалуйста, выберите жанр, используя клавиатуру ниже."
        )
        return

    logger.info(f'Пользователь [{message.from_user.id}]  '
                f'выбрал действия filter_genre [{message.text.lower()}]')

    data_anime = await ApiClient().get_filter_genre(message.text.lower())

    if not data_anime:
        await message.answer('Что-то пошло не так!!!')
        await state.finish()
        logger.error(f'Данные с сервера неверны запрос '
                     f'[get_filter_genre({message.text.lower()})]')
        return

    await message.answer(
        f"<b>Жанр</b>: \t {message.text.lower()}\n"
        f"<b>Количество</b>: \t {data_anime['count']} аниме",
        parse_mode=types.ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )

    count = data_anime['count'] / 20
    page_list = [x for x in reversed(range(1, math.ceil(count) + 1))]
    genre = message.text.lower()
    await state.update_data(page_list=page_list, genre=genre)
    await FilterGenre.next()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Показать страницу')
    keyboard.add('Отмена')
    await message.answer('Выберете действия:', reply_markup=keyboard)


async def pagination(message: types.Message, state: FSMContext):
    if message.text.lower() == 'показать страницу':
        user_data = await state.get_data()

        if user_data['page_list']:
            data = await ApiClient().get_filter_genre(
                user_data['genre'],
                user_data['page_list'][-1]
            )
            for item in data['results']:
                await message.answer_photo(
                    item['url_image_preview'],
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


def register_handlers_filter_genre(dp: Dispatcher):
    dp.register_message_handler(
        filter_genre_start,
        commands='filter_genre',
        state='*'
    )
    dp.register_message_handler(
        filter_genre_result,
        state=FilterGenre.waiting_for_genre
    )
    dp.register_message_handler(
        pagination,
        state=FilterGenre.waiting_for_page
    )