from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from keyboards.keyboard_utils.schema_generator import create_keyboard_layout
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data.config import settings
from utils.sharpdll.sharpdll import GoogleUtils, Session, System, REGEX_EXPONENTIAL
from System.Collections.Generic import List
import re
import math

ts = [63.6567, 9.9248, 5.8409]


class DataInput(StatesGroup):
    session_data = State()
    input_session_number = State()
    input_td = State()
    input_od = State()


async def input_td(callback: CallbackQuery):
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
        text='Введите номер сеанса и значения по одному в строке:\n\n'
             'Введите /cancel для отмены'
    )
    await DataInput.input_td.set()


async def change_td(msg: types.Message, state: FSMContext):
    args = list(map(str, msg.text.split('\n')))
    if msg.text == '/cancel':
        await msg.answer("Отмена")
        await state.reset_state()
    else:
        try:
            await state.set_data({'td': args.copy()})
            if len(args) < 3 or len(args) > 10:
                await msg.answer('Неверные данные. Попробуйте ещё раз.')
            else:
                google = GoogleUtils(settings.SERVICE_ACCOUNT_EMAIL,
                                    settings.SERVICE_CREDS,
                                    settings.GOOGLE_APP_NAME)
                detectors = List[float]()
                for val in args[1:]:
                    detectors.Add(float(str(val).lower().replace(',', '.')))
                google.SetTrackDetectorsInfo(settings.SPREADSHEET_ID, int(args[0]), detectors)
                set_measure_results(int(args[0]))
                await msg.answer(f'Введены значения ТД для сеанса {args[0]}: {" / ".join(args[1:])}')
                await state.reset_state()

        except Exception as e:
            print(e)
            await msg.answer('Неверные данные. Попробуйте ещё раз.')


async def input_od(callback: CallbackQuery):
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
        text='Введите номер сеанса и значения по одному в строке:\n\n'
             'Введите /cancel для отмены'
    )
    await DataInput.input_od.set()


async def change_od(msg: types.Message, state: FSMContext):
    args = list(map(str, msg.text.split('\n')))
    if msg.text == '/cancel':
        await msg.answer("Отмена")
        await state.reset_state()
    else:
        try:
            await state.set_data({'od': args.copy()})
            if len(args) != 5:
                await msg.answer('Неверные данные. Попробуйте ещё раз.')
            else:
                google = GoogleUtils(settings.SERVICE_ACCOUNT_EMAIL,
                                    settings.SERVICE_CREDS,
                                    settings.GOOGLE_APP_NAME)
                detectors = List[float]()
                for val in args[1:]:
                    detectors.Add(float(str(val).lower().replace(',', '.')))
                google.SetOnlineDetectorsInfo(settings.SPREADSHEET_ID, int(args[0]), detectors)
                set_measure_results(int(args[0]))
                await msg.answer(f'Введены значения ОД для сеанса {args[0]}: {" / ".join(args[1:])}')

            await state.reset_state()

        except Exception as e:
            print(e)
            await msg.answer('Неверные данные. Попробуйте ещё раз.')

async def set_measure_results(session_id: int):
    google = GoogleUtils(settings.SERVICE_ACCOUNT_EMAIL,
                         settings.SERVICE_CREDS,
                         settings.GOOGLE_APP_NAME)
    index = google.GetIndexBySessionNumber(settings.SPREADSHEET_ID, "Data", session_id)
    tds = google.GetValuesFromRange(settings.SPREADSHEET_ID, f"Data!I{index}:Q{index}")[0]
    ods = google.GetValuesFromRange(settings.SPREADSHEET_ID, f"Data!S{index}:V{index}")[0]
    print(len(tds), len(ods))
    if len(tds) > 1 and len(ods) == 4:
        ods_avg = sum([float(str(od).lower().replace(',','.')) for od in ods])/len(ods)
        ks = [float(str(td).lower().replace(',','.'))/ods_avg for td in tds]
        avg_k = sum(ks)/len(ks)
        sigma = math.sqrt((sum([ki - avg_k for ki in ks])**2)/len(ks))
        ip = avg_k*0.28
        t = ts[len(tds)-2]
        error = math.sqrt((sigma*t)**2 + ip**2)
        all_max = max([float(str(td).lower().replace(',','.')) for td in tds])
        all_min = min([float(str(td).lower().replace(',','.')) for td in tds])
        heterogeneity = ((all_max - all_min)/all_max)*100
        heterogeneity_left = -1
        heterogeneity_right = -1
        if len(tds) == 4:
            all_max = max([float(str(td).lower().replace(',','.')) for td in tds[:2]])
            all_min = min([float(str(td).lower().replace(',','.')) for td in tds[:2]])
            heterogeneity_left = ((all_max - all_min)/all_max)*100
            all_max = max([float(str(td).lower().replace(',','.')) for td in tds[2:]])
            all_min = min([float(str(td).lower().replace(',','.')) for td in tds[2:]])
            heterogeneity_right = ((all_max - all_min)/all_max)*100
        google.SetMeasureResults(settings.SPREADSHEET_ID, session_id, avg_k, error, heterogeneity,
                                 heterogeneity_left, heterogeneity_right)