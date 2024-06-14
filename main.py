#Импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from config import TOKEN
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import keyboard as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from openpyxl import load_workbook
from aiogram.types.input_file import FSInputFile
import sqlite3

#База бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

#Состояния бота
class Send(StatesGroup):
    name = State()
    locate = State()
    problem = State()

#Реагирование на старт
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Нажми на "Оставьте заявку", и опиши свою проблему', reply_markup=kb.main)

#Реагирование на кнопку Описать проблему
@dp.message(F.text == "Оставьте заявку")
async def pipi(message: Message, state: FSMContext):
    await state.set_state(Send.name)   
    await message.answer(text=f"Отправьте свое ФИО")

#Ввод имени и загрузка данных в локальное хранилище
@dp.message(Send.name)
async def pipi(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Send.locate) 
    await message.answer(text=f"Укажите ваш кабинет (Только цифры, пример: 233)")


#Ввод локации и загрузка данных в локальное хранилище
@dp.message(Send.locate)
async def pipi(message: Message, state: FSMContext):
    await state.update_data(locate=message.text)
    await state.set_state(Send.problem) 
    await message.answer(text=f"Проблема", reply_markup=kb.another)

#Выбор другой проблемы и запись данных в локальное хранилище
@dp.message(F.text == "Другая проблема")
async def pipi(message: Message, state: FSMContext):
    await state.set_state(Send.problem) 
    await message.answer(text=f"Кратко опишите свою проблему") 

@dp.message(Send.problem)
async def pipi(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    #Выгрузка данных из хранилища
    data = await state.get_data()
    
    #Конект с бд
    db = sqlite3.connect('tasks.db')

    c = db.cursor()

    #Команда внесение данных
    c.execute(f"INSERT INTO tasks (name, locate, problem, status) VALUES ('{data['name']}', '{data['locate']}', '{data['problem']}', 'Отправлен')")

    data['last_id'] = c.lastrowid

    #Потверждение вноса
    db.commit()

    #Закрытие конекта
    db.close()
    
    #Отправка данных пользователю
    await message.answer(text=f"Ваш запрос отправлен!", reply_markup=kb.main)
    await message.answer(text=f"******************************\n\nИмя: {data['name']}\nМесто: {data['locate']}\nПроблема: {data['problem']}\n\n******************************")
    
    #Отправка данных админу
    await bot.send_message(chat_id="830213240", text=f"******************************\n\nИмя: {data['name']}\nМесто: {data['locate']}\nПроблема: {data['problem']}\n\n******************************\n\n /task_{data['last_id']}", reply_markup=kb.inlain)
    
    #Сброс состояния
    await state.clear()

    #запись в exel
    #fn = "help\\1.xlsx"
    #wb = load_workbook(fn)
    #ws = wb['data']
    #ws.append([f"Имя",f"Место",f"Проблема"])
    #ws.append([f"{data['name']}",f"{data['locate']}",f"{data['problem']}"])
    #ws.append([f"",f"",f""])
    #wb.save(fn)
    #wb.close()

    #Отправка exel файла
    #document = FSInputFile('help\\1.xlsx')
    #await bot.send_document("808721429", document)

    

#Удаление запроса, при выполнении(админ)
@dp.callback_query(F.data == "yes")
async def dow(callback: CallbackQuery):
     await callback.message.delete()

#Реакция на неизвестную команду
@dp.message()
async def cmd(message: Message):
    await message.answer("Неизвестная команда")
    await message.delete()

#База бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

#База бота
if __name__ == '__main__':
    asyncio.run(main()) 