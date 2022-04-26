from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from utils.sharpdll.sharpdll import GoogleUtils
from data.config import settings


async def bot_start(msg: types.Message):
    if await check_user_staff(msg) is False:
        await msg.bot.send_message(
            chat_id=msg.from_user.id,
            text='Вы не имеете доступа к боту.'
        )
    else:
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
            text=f'Выберите действие:',
            reply_markup=markup
        )

async def check_user_staff(msg: types.Message):
    google = GoogleUtils(settings.GOOGLE_API_KEY, settings.GOOGLE_APP_NAME)
    users_info = google.GetValuesFromRange(settings.SPREADSHEET_ID, "Staff!A:B")
    for row in users_info:
        if msg.from_user.username == str(row[1]).replace('@','') or msg.from_user.id == row[0]:
            return True
    return False