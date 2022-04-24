from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class DataInput(StatesGroup):
    session_data = State()
    input_session_number = State()
    input_td = State()
    input_od = State()
    input_k = State()
    input_plus_minus = State()
    input_left = State()
    input_right = State()


async def input_td(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значения:',
        reply_markup=markup
    )
    await DataInput.input_td.set()


async def change_td(msg: types.Message, state: FSMContext):
    args = list(map(str, msg.text.split('\n')))

    try:
        await state.set_data({'td': args.copy()})
        await msg.answer(f'Перезапуск /start\nВведены значения ТД: {" - ".join(args)}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_od(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значения:',
        reply_markup=markup
    )
    await DataInput.input_od.set()


async def change_od(msg: types.Message, state: FSMContext):
    args = list(map(str, msg.text.split('\n')))

    try:
        await state.set_data({'od': args.copy()})
        await msg.answer(f'Перезапуск /start\nВведены значения ОД: {" / ".join(args)}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_k(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значение:',
        reply_markup=markup
    )
    await DataInput.input_k.set()


async def change_k(msg: types.Message, state: FSMContext):
    coefficient_k = msg.text

    try:
        await state.set_data({'k': float(coefficient_k)})
        await msg.answer(f'Перезапуск /start\nВведено значение К: {coefficient_k}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_plus_minus(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значение:',
        reply_markup=markup
    )
    await DataInput.input_plus_minus.set()


async def change_plus_minus(msg: types.Message, state: FSMContext):
    coefficient_plus_minus = msg.text

    try:
        await state.set_data({'k': float(coefficient_plus_minus)})
        await msg.answer(f'Перезапуск /start\nВведено значение коэффициента +/: {coefficient_plus_minus}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_left(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значение:',
        reply_markup=markup
    )
    await DataInput.input_left.set()


async def change_left(msg: types.Message, state: FSMContext):
    coefficient_left_side = msg.text

    try:
        await state.set_data({'k': float(coefficient_left_side)})
        await msg.answer(f'Перезапуск /start\nВведено значение неопределенности по левой стороне: {coefficient_left_side}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_right(callback: CallbackQuery):
    buttons = [

    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [0]):
        markup.row(*row)
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

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text='Введите значение:',
        reply_markup=markup
    )
    await DataInput.input_right.set()


async def change_right(msg: types.Message, state: FSMContext):
    coefficient_right_side = msg.text

    try:
        await state.set_data({'right_side': float(coefficient_right_side)})
        await msg.answer(f'Перезапуск /start\nВведено значение неопределенности по правой стороне: {coefficient_right_side}')
        await state.reset_state()

    except Exception as e:
        await msg.answer('Неверные данные. Попробуйте ещё раз.')
