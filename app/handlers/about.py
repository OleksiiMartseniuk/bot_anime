import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from service.api import ApiClient

from ..keyboards import reply
from ..states.about import AboutMessage


logger = logging.getLogger(__name__)


async def about_start(message: types.Message):
    """О боте"""
    logger.info(f'Пользователь [{message.from_user.id}] '
                f'выбрал действия [about]')

    # Запись статистики
    await ApiClient().sent_statistic(
        message.from_user.id,
        'about',
        'О боте'
    )

    await AboutMessage.waiting_for_star_about.set()
    keyboard = reply.get_about()
    await message.answer('Данный проект на этапе разработке. '
                         'Если есть какие-то вопросы, пожелания напишите нам,'
                         ' ми будем очень благодарны.\n'
                         'Хорошего дня)', reply_markup=keyboard)


async def write_message(message: types.Message, state: FSMContext):
    """Проверка на выбор действия"""
    if message.text.lower() != 'отправить сообщения':
        await message.answer(
            "Пожалуйста, выберите действия, используя клавиатуру ниже."
        )
        return
    await message.answer(
        'Введите текст сообщения....✍️',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await AboutMessage.next()


async def send_message(message: types.Message, state: FSMContext):
    """Запись сообщения в db"""
    result = await ApiClient().sent_message(message.from_user.id, message.text)
    if not result:
        await message.answer('Что-то пошло не так!!!')
        logger.error('Переменная result пуста')
        await state.finish()
        return
    await message.answer('Сообщения отправлено 📬')
    await message.answer('Спасибо за потраченное время !!!')
    await state.finish()


def register_handlers_about(dp: Dispatcher):
    dp.register_message_handler(
        about_start,
        commands="about",
        state="*"
    )
    dp.register_message_handler(
        write_message,
        state=AboutMessage.waiting_for_star_about
    )
    dp.register_message_handler(
        send_message,
        state=AboutMessage.waiting_for_write_massage
    )
