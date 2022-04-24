from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class DataInput(StatesGroup):
    session_data = State()


async def add_session(callback: CallbackQuery):
    buttons = [

    ]

    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
    try:
        # await callback.bot.edit_message_text(
        #     text=callback.message.text + '\nВыбрано "Составить протокол"',
        #     chat_id=callback['from'].id,
        #     message_id=callback.message.message_id,
        #     reply_markup=None
        # )
        await callback.bot.delete_message(callback['from'].id, callback.message.message_id)
    except Exception as e:
        pass

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите данные:\n'
             '1. Номер сеанса\n'
             '2. Название организации\n'
             '3. Объект испытаний\n'
             '4. Код среды\n'
             '5. Угол облучения\n'
             '6. Давление\n'
             '7. Влажность\n'
             '8. Температура на испытательном комплексе\n'
             '9. Температура в сеансе',
        reply_markup=markup
    )
    await DataInput.session_data.set()


async def session_data(msg: types.Message, state: FSMContext):
    args = list(map(str, msg.text.split('\n')))
    await msg.answer('/start\nВведены данные:\n' + ' - '.join(args))
    await state.reset_state()
