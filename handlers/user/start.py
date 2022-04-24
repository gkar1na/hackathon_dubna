from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def bot_start(msg: types.Message):
    buttons = [
        InlineKeyboardButton(
            text='Составить протокол',
            callback_data='draw_up_protocol'
        ),
        InlineKeyboardButton(
            text='Добавить сеанс',
            callback_data='add_session'
        ),
        InlineKeyboardButton(
            text='Изменить сеанс',
            callback_data='change_session'
        )
    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [1, 2]):
        markup.row(*row)

    if isinstance(msg, CallbackQuery):
        try:
            # await callback.bot.edit_message_text(
            #     text=callback.message.text + '\nДействие сброшено.',
            #     chat_id=callback['from'].id,
            #     message_id=callback.message.message_id,
            #     reply_markup=None
            # )
            await msg.bot.delete_message(msg['from'].id, msg.message.message_id)
        except Exception as e:
            pass
    await msg.bot.send_message(
        chat_id=msg.from_user.id,
        text=f'Привет, {msg.from_user.full_name}!',
        reply_markup=markup
    )
