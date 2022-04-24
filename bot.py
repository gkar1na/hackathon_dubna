import asyncio
from typing import List, Tuple

import aiogram.utils.executor
import aiojobs as aiojobs
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from aiohttp import web
from loguru import logger

from data.config import settings


# noinspection PyUnusedLocal
async def on_startup(app: web.Application):
    import middlewares
    import filters
    import handlers
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    await handlers.user.setup(dp)
    logger.info('Configure Webhook URL to: {url}', url=settings.WEBHOOK_URL)
    await dp.bot.set_webhook(settings.WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
    await app_bot.close()


async def init() -> web.Application:
    from utils.misc import logging
    import web_handlers
    logging.setup()
    scheduler = await aiojobs.create_scheduler()
    app = web.Application()
    subapps: List[Tuple[str, web.Application]] = [
        ('/tg/webhooks/', web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp['bot'] = bot
        subapp['dp'] = dp
        subapp['scheduler'] = scheduler
        app.add_subapp(prefix, subapp)

        app['bot'] = bot
        app['dp'] = dp
        app['scheduler'] = scheduler

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == '__main__':
    bot = Bot(settings.TG_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = RedisStorage2(**settings.REDIS)
    dp = Dispatcher(bot, storage=storage)

    web.run_app(app=init())
