from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class DataInput(StatesGroup):
    session_data = State()
    input_session_number = State()
    choice_change_data = State()


async def change_session(callback: CallbackQuery):
    try:
        # await callback.bot.edit_message_text(
        #     text=callback.message.text + '\nВыбрано "Изменить сеанс"',
        #     chat_id=callback['from'].id,
        #     message_id=callback.message.message_id,
        #     reply_markup=None
        # )
        await callback.bot.delete_message(callback['from'].id, callback.message.message_id)
    except Exception as e:
        pass

    await choice_change_data(callback)


async def input_session_number(msg: types.Message, state: FSMContext):
    session_number = msg.text

    try:
        await state.set_data({'session_number': int(msg.text)})
        await msg.answer(f'Введен номер сессии: {session_number}')
        #await state.reset_state()
        

    except Exception as e:
        print(e)
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def choice_change_data(callback: CallbackQuery):
    buttons = [
        InlineKeyboardButton(
            text='ТД1-9',
            callback_data='td1_9'
        ),
        InlineKeyboardButton(
            text='ОД1-4',
            callback_data='od1_4'
        )
    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [1,1]):
        markup.row(*row)

    await callback.message.bot.send_message(
        chat_id=callback['from'].id,
        text='Выберите параметр, который хотите изменить:',
        reply_markup=markup
    )
