import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.handlers.schedules import register_handlers_schedules
from app.handlers.common import register_handlers_common

from settings import TOKEN_BOT


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Команды бота"""
    commands = [
        BotCommand(command="/anime_schedules", description="Расписания"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_schedules(dp)
    register_handlers_common(dp)
    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
