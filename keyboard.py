from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#Добавление первой кнопки
main = ReplyKeyboardMarkup(keyboard=

[                              
    [KeyboardButton(text="Оставьте заявку")],

],resize_keyboard=True
)

#Добавление кнопок проблем
another = ReplyKeyboardMarkup(keyboard=

[                              
    [KeyboardButton(text="Не работает принтер")],
    [KeyboardButton(text="Не работает компьютер")],
    [KeyboardButton(text="Не работает интернет")],
    [KeyboardButton(text="Другая проблема")],

],resize_keyboard=True
)


#Инлайн кнопка админа
inlain = InlineKeyboardMarkup(inline_keyboard=

[                              
    [InlineKeyboardButton(text="Принять", callback_data="yes")],
    [InlineKeyboardButton(text="Проблема ⛔", callback_data="yes")],
    [InlineKeyboardButton(text="Готово ✅", callback_data="yes")]

],resize_keyboard=True
)