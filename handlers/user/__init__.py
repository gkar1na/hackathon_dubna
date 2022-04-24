from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from .help import bot_help
from .start import bot_start
from .draw_up_protocol import draw_up_protocol
from .access_protocol import access_protocol
from .add_session import add_session, session_data
from .monitoring_protocol import monitoring_protocol
from .change_session import change_session, input_session_number, choice_change_data
from .input_session_data import *


class DataInput(StatesGroup):
    session_data = State()
    input_session_number = State()
    input_td = State()
    input_od = State()
    input_k = State()
    input_plus_minus = State()
    input_left = State()
    input_right = State()


async def setup(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand('start', 'restart'),
            BotCommand('help', 'info')
        ]
    )
    dp.register_message_handler(bot_start, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())

    dp.register_callback_query_handler(
        bot_start,
        lambda query: query.data == 'start'
    )
    dp.register_callback_query_handler(
        draw_up_protocol,
        lambda query: query.data == 'draw_up_protocol'
    )
    dp.register_callback_query_handler(
        access_protocol,
        lambda query: query.data == 'access_protocol'
    )
    dp.register_callback_query_handler(
        monitoring_protocol,
        lambda query: query.data == 'monitoring_protocol'
    )

    dp.register_callback_query_handler(
        add_session,
        lambda query: query.data == 'add_session'
    )
    dp.register_message_handler(
        callback=session_data,
        state=DataInput.session_data
    )

    dp.register_callback_query_handler(
        change_session,
        lambda query: query.data == 'change_session'
    )
    dp.register_message_handler(
        callback=input_session_number,
        state=DataInput.input_session_number
    )

    dp.register_callback_query_handler(
        input_td,
        lambda query: query.data == 'td1_9'
    )
    dp.register_message_handler(
        callback=change_td,
        state=DataInput.input_td
    )

    dp.register_callback_query_handler(
        input_od,
        lambda query: query.data == 'od1_4'
    )
    dp.register_message_handler(
        callback=change_od,
        state=DataInput.input_od
    )

    dp.register_callback_query_handler(
        input_k,
        lambda query: query.data == 'coefficient_k'
    )
    dp.register_message_handler(
        callback=change_k,
        state=DataInput.input_k
    )

    dp.register_callback_query_handler(
        input_plus_minus,
        lambda query: query.data == 'coefficient_+-'
    )
    dp.register_message_handler(
        callback=change_plus_minus,
        state=DataInput.input_plus_minus
    )
    dp.register_callback_query_handler(
        input_left,
        lambda query: query.data == 'coefficient_left_side'
    )
    dp.register_message_handler(
        callback=change_left,
        state=DataInput.input_left
    )
    dp.register_callback_query_handler(
        input_right,
        lambda query: query.data == 'coefficient_right_side'
    )
    dp.register_message_handler(
        callback=change_right,
        state=DataInput.input_right
    )
