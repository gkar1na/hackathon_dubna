from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def access_protocol(callback: CallbackQuery):
    buttons = [
        InlineKeyboardButton(
            text='К выбору протокола',
            callback_data='draw_up_protocol'
        ),
        InlineKeyboardButton(
            text='Сброс',
            callback_data='start'
        )
    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [1, 1]):
        markup.row(*row)
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
        text='#TODO draw up a protocol -> access protocol',
        reply_markup=markup
    )
