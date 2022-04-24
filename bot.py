import asyncio
from typing import List, Tuple

import aiogram.utils.executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from loguru import logger

from data.config import settings


# noinspection PyUnusedLocal
async def on_startup(dp: Dispatcher):
    from utils.misc import logging
    import middlewares
    import filters
    import handlers
    logging.setup()

    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    await handlers.user.setup(dp)


if __name__ == '__main__':
    bot = Bot(settings.TG_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    # storage = RedisStorage2(**settings.REDIS)
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    aiogram.utils.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
