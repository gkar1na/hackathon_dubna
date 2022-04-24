from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from .help import bot_help
from .start import bot_start


async def setup(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'restart'),
            BotCommand('help', 'make help')
        ]
    )
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())
