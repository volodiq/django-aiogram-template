import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs

from app.root_router import root_router
from providers import env
from providers.bot import bot
from providers.logger import InterceptHandler, logger


async def main():
    fsm_storage = RedisStorage.from_url(
        env.redis_fsm_dsn,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp = Dispatcher(storage=fsm_storage)
    dp.include_router(root_router)
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    logger.info("Starting bot...")
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    asyncio.run(main())
