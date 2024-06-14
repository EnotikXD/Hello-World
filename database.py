#import asyncio 
import sqlite3

data = {
    'name':'Sasha',
    'locate':'19',
    'problem':'Printer'
    }
#Конект с бд
db = sqlite3.connect('tasks.db')

c = db.cursor()

#Команда внесение данных
c.execute(f"INSERT INTO tasks (name, locate, problem, status) VALUES ('{data['name']}', '{data['locate']}', '{data['problem']}','Отправлен' )")

#Потверждение вноса
db.commit()

#Закрытие конекта
db.close()