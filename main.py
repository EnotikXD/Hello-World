#Импорт библиотек
from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from openpyxl import load_workbook

#Токен
TOKEN_API = "7070062861:AAFsL-BiesivWl0HLhBYvn2PvsqiC1grALU"

#База бота
storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

#Состояния бота
class ProfileStatesGroup(StatesGroup):

    name = State()
    locate = State()
    problem = State()
    

#Добавление первой кнопки
def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('⚙️Описать проблему⚙️'))
    return kb

#Добавление кнопок проблем
def get_kb2() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Принтер💣'))
    kb.add(KeyboardButton('Влетел компьютер💥'))
    kb.add(KeyboardButton('Интернет r.i.p☠️'))
    kb.add(KeyboardButton('Другая проблема🛠'))
    return kb

#Инлайн кнопка админа
ikb = InlineKeyboardMarkup(row_width=2)
ibut1 = InlineKeyboardButton(text="Сделать✅", callback_data="yes")
ikb.add(ibut1)

#Реагирование на старт
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Нажми на "Описать проблему", и опиши свою проблему', reply_markup=get_kb())

#Реагирование на кнопку создать
@dp.message_handler(text=['⚙️Описать проблему⚙️'])
async def cmd_create(message: types.Message) -> None:
    await message.answer("Отправьте свое ФИО")
    await ProfileStatesGroup.name.set()  # установили состояние имя

#Ввод имени и загрузка данных в локальное хранилище
@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Место проблемы📍')
    await ProfileStatesGroup.next()

#Ввод локации и загрузка данных в локальное хранилище
@dp.message_handler(state=ProfileStatesGroup.locate)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['locate'] = message.text

    await message.answer('С какой проблемой вы столкнулись ?', reply_markup=get_kb2())
    await ProfileStatesGroup.next()

#Выбор другой проблемы и запись данных в локальное хранилище
@dp.message_handler(state=ProfileStatesGroup.problem, text = ['Другая проблема🛠'])
async def load_desc(message: types.Message, state: FSMContext) -> None:
    await message.answer('Кратко опишите свою проблему')
    async with state.proxy() as data:
        data['problem'] = message.text
    

#Ввод проблемы и загрузка данных в локальное хранилище
@dp.message_handler(state=ProfileStatesGroup.problem)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['problem'] = message.text
        #Выгрузка данных из хранилища
        await bot.send_message(chat_id=message.from_user.id, text=f"******************************\n\nИмя: {data['name']}\nМесто: {data['locate']}\nПроблема: {data['problem']}\n\n******************************", reply_markup=get_kb())
        
        await message.answer('Ваш запрос создан!')

        #Отправка данных админу
        await bot.send_message(chat_id="808721429", text=f"******************************\n\nИмя: {data['name']}\nМесто: {data['locate']}\nПроблема: {data['problem']}\n\n******************************", reply_markup=ikb)

        #запись в exel
        fn = "1.xlsx"
        wb = load_workbook(fn)
        ws = wb['data']
        ws.append([f"Имя",f"Место",f"Проблема"])
        ws.append([f"{data['name']}",f"{data['locate']}",f"{data['problem']}"])
        ws.append([f"",f"",f""])
        wb.save(fn)
        wb.close()

        #Отправка exel файла
        await bot.send_document(chat_id= "808721429", document  = open('1.xlsx', 'rb')) 

    #Сброс состояния
    await state.finish()

#Удаление запроса, при выполнении(админ)
@dp.callback_query_handler(text="yes")
async def dow(callback: types.CallbackQuery):
     await callback.message.delete()

#Реакция на неизвестную команду
@dp.message_handler()
async def cmd_create(message: types.Message) -> None:
    await message.answer("Неизвестная команда😢")
    await message.delete()

#База бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)