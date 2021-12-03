from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram.utils import executor

from config import dp
from keyboards import enter_num
from db_func import search_by_db


class NumState(StatesGroup):
    q1 = State()
    q2 = State()


@dp.message_handler(Text(equals='Начать'))
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    user = message.from_user.full_name
    text = f'Привет, {user}, для поиска совпадений воспользуйтесь кнопочным меню или командами:\n' \
           f'<b>/num</b> - найти совпадения по номеру;\n' \
           f'<b>/photo</b> - найти совпадения по фото.'
    await message.answer(text, reply_markup=enter_num)


@dp.message_handler(filters.CommandHelp())
@dp.message_handler(text='Помощь')
async def cmd_help(message: types.Message):
    text = 'Для поиска совпадений воспользуйтесь <i>кнопочным меню</i> или <i>командами</i>:\n' \
           f'<b>/num</b> - найти совпадения по номеру;\n' \
           f'<b>/photo</b> - найти совпадения по фото.\n\n' \
           f'В случае отсутствия меню - введите команду <b>/start</b>.'
    await message.answer(text, reply_markup=enter_num)


@dp.message_handler(Text(equals='Текстом'))
@dp.message_handler(commands='num')
async def cmd_num(message: types.Message):
    await message.answer('Введите номер в формате "<b>А999АА999</b>".')
    await NumState.q1.set()


@dp.message_handler(state=NumState.q1)
async def answer_num_text(message: types.Message, state: FSMContext):
    car_num = message.text.upper()
    car_info = search_by_db(car_num)
    if car_info is not None:
        await message.answer(f'По номеру <b>{car_num}</b> найдено совпадение:\n'
                             f'Актив банка: <i>{car_info[0]}.</i>')
    else:
        await message.answer('Совпадений по номеру не найдено.')
    await state.finish()


@dp.message_handler(content_types=ContentType.ANY)
async def other_msg(message: types.Message):
    await message.answer("Ваш запрос не понятен!\n"
                         "Воспользуйтесь командами или кнопочным меню.\n\n"
                         "В случае отсутствия меню - введите команду <b>/start</b>.")


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
