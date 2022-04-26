from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from utils.sharpdll.sharpdll import GoogleUtils, Session, System, REGEX_EXPONENTIAL
import re
from data.config import settings


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
        text=f'Введите данные:\n'
             '1. Название организации (или же ПН(переход), ПН(смена))\n'
             '2. Объекты испытаний (4 шт.)\n'
             '3. Код среды\n'
             '4. Угол облучения\n'
             '5. Давление\n'
             '6. Влажность\n'
             '7. Температура на испытательном комплексе\n'
             '8. Температура в сеансе\n'
             '9. Начало сеанса\n'
             '10. Конец сеанса\n'
             '11. Длительность облучения\n'
             '12. Интенсивность потока\n'
             '13. Номер протокола допуска (для сеансов типа ПН)\n\n'
             'Введите /cancel для отмены операции',
        reply_markup=markup
    )
    await DataInput.session_data.set()


async def session_data(msg: types.Message, state: FSMContext):
    google = GoogleUtils(settings.SERVICE_ACCOUNT_EMAIL,
                         settings.SERVICE_CREDS,
                         settings.GOOGLE_APP_NAME)
    args = list(map(str, msg.text.split('\n')))
    if msg.text in ['/cancel']:
        await msg.answer("Отмена")
        await state.reset_state()
    else:
        if len(args) != 12 or args[1].startswith('ПН') and len(args) != 13:
            await msg.answer("Неверные данные, попробуйте еще раз")
        else:
            try:
                new_session_id = int(google.GetValuesFromRange(settings.SPREADSHEET_ID, "Data!A1:A")[-1][0])+1
                if args[0].startswith('ПН'):
                    session_info = Session(new_session_id, args[0], args[1].split(' '), args[2],
                                        args[12], float(args[3]), float(args[4]), float(args[5]),
                                        float(args[6]), float(args[7]), System.DateTime.Parse(args[8]),
                                        System.DateTime.Parse(args[9]), System.TimeSpan.Parse(args[10]))
                else:
                    values = google.GetValuesFromRange(settings.SPREADSHEET_ID,
                                                       "Data!B1:X")
                    adm_prot_code = ""
                    for i in range(len(values) - 1, -1, -1):
                        if str(values[i][0]).startswith("ПН") and str(values[i][21]) == "2,00E+04":
                            adm_prot_code = str(values[i][22])
                            break
                    session_info = Session(new_session_id, str(args[0]), args[1].split(' '), str(args[2]),
                                        adm_prot_code, float(args[3]), float(args[4]), float(args[5]),
                                        float(args[6]), float(args[7]), System.DateTime.Parse(args[8]),
                                        System.DateTime.Parse(args[9]), System.TimeSpan.Parse(args[10]))
                if re.match(REGEX_EXPONENTIAL, args[11].lower()) is not None:
                    session_info.StreamIntensity = float(str(args[11].lower().replace(',','.')))
                else:
                    session_info.StreamIntensity = float(args[11])
                google.SetNewSessionInfo(settings.SPREADSHEET_ID,
                                        session_info)
                await msg.answer(f'Введены данные для сеанса {new_session_id}:\n' + ' - '.join(args) + '\n\nСеанс добавлен.')
            except Exception as e:
                print(e)
                await msg.answer("Неверные данные, попробуйте еще раз")
            await state.reset_state()
