import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.handlers.schedules import register_handlers_schedules
from app.handlers.anons import register_handlers_anons
from app.handlers.common import register_handlers_common
from app.handlers.search import register_handlers_search
from app.handlers.filter_genre import register_handlers_filter_genre
from app.handlers.about import register_handlers_about
from app.handlers.timeline import register_handlers_timeline
from app.handlers.profile import register_handlers_profile

from config.settings import TOKEN_BOT


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Команды бота"""
    commands = [
        BotCommand(command="/profile", description="Профиль"),
        BotCommand(command="/schedules", description="Расписания"),
        BotCommand(command="/timeline", description="Лента"),
        BotCommand(command="/anons", description="Анонс"),
        BotCommand(command="/search", description="Поиск"),
        BotCommand(command="/filter_genre", description="Фильтр по жанрам"),
        BotCommand(command="/about", description="О нас"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_schedules(dp)
    register_handlers_common(dp)
    register_handlers_anons(dp)
    register_handlers_search(dp)
    register_handlers_filter_genre(dp)
    register_handlers_about(dp)
    register_handlers_timeline(dp)
    register_handlers_profile(dp)

    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
