import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope import BotCommandScopeDefault
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config_loader import Config, load_config
from handlers.dices import dices_handlers
from db.base import Base
from middlewares.throttling import ThrottlingMiddleware
from updatesworker import get_handled_updates_list


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Перезапустить казино"),
        BotCommand(command="spin",
                   description="Показать клавиатуру и сделать бросок"),
        BotCommand(command="stop", description="Убрать клавиатуру"),
        BotCommand(command="help", description="Справочная информация")
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    config: Config = load_config()

    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}",
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    storage = MemoryStorage()
    bot = Bot(config.bot.token, parse_mode="HTML")
    bot["db"] = async_sessionmaker
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(ThrottlingMiddleware())

    dices_handlers(dp)

    await set_bot_commands(bot)

    try:
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.error("Bot stopped!")
