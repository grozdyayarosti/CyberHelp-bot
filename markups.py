from telebot import types

main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Инициализация альтернативной клавиатуры
# TODO добавить one_time_keyboard=True в аргументы выше
btn1 = types.KeyboardButton('Проверка ссылок') # Добавление кнопки
btn2 = types.KeyboardButton('Справка по безопасности')
btn3 = types.KeyboardButton('Генерация пароля')
main_menu_markup.row(btn1, btn2, btn3)

to_home_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Инициализация альтернативной клавиатуры
to_home_btn = types.KeyboardButton('Вернуться к меню') # Добавление кнопки
to_home_markup.row(to_home_btn)
