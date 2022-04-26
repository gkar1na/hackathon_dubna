from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def draw_up_protocol(callback: CallbackQuery):
    buttons = [
        InlineKeyboardButton(
            text='Протокол допуска',
            callback_data='access_protocol'
        ),
        InlineKeyboardButton(
            text='Протокол мониторинга',
            callback_data='monitoring_protocol'
        ),
        InlineKeyboardButton(
            text='В начало',
            callback_data='start'
        )
    ]
    markup = InlineKeyboardMarkup()
    for row in create_keyboard_layout(buttons, [2, 1]):
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
        text='Выберите тип протокола:',
        reply_markup=markup
    )
