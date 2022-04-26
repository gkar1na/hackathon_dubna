from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from utils.sharpdll.sharpdll import DocumentUtils
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data.config import settings
import os

class DataInput(StatesGroup):
    session_data = State()
    input_session_number = State()
    input_td = State()
    input_od = State()
    input_k = State()
    input_plus_minus = State()
    input_left = State()
    input_right = State()
    input_access_protocol = State()


async def create_markup():
    buttons = [
        InlineKeyboardButton(
            text='К выбору протокола',
            callback_data='draw_up_protocol'
        ),
        InlineKeyboardButton(
            text='В начало',
            callback_data='start'
        )
    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [1, 1]):
        markup.row(*row)
    return markup

async def access_protocol(callback: CallbackQuery):
    try:
        # await callback.bot.edit_message_text(
        #     text=callback.message.text + '\nВыбрано "Протокол допуска"',
        #     chat_id=callback['from'].id,
        #     message_id=callback.message.message_id,
        #     reply_markup=None
        # )
        await callback.bot.delete_message(callback['from'].id, callback.message.message_id)
    except Exception as e:
        pass

    await callback.bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите номер сеанса"
    )
    await DataInput.input_access_protocol.set()

async def create_new_access_protocol(msg: types.Message, state: FSMContext):
    doc_utils = DocumentUtils(settings.GOOGLE_API_KEY,
                              settings.GOOGLE_APP_NAME)
    try:
        sessionId = int(msg.text)
        path = doc_utils.CreateAdmissionReport(settings.SPREADSHEET_ID,
                                               sessionId)
        await msg.bot.send_document(
            chat_id=msg.from_user.id,
            document=InputFile(f"{path}"),
            caption="Ваш документ:"
        )
        os.remove(path)
        await msg.bot.send_message(
            chat_id=msg.from_user.id,
            text="Выберите действие:",
            reply_markup=await create_markup()
        )
        await state.reset_state()
    except Exception as e:
        await msg.answer("Неверные данные, попробуйте еще раз")
        print(e)
    
