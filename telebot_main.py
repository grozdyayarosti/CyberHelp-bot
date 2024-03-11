import telebot
from telebot import types

from funcs import key_word_search

bot = telebot.TeleBot('6917064050:AAH11UnUNTaC47hBb9VjwRjm5wLZPtUD5H8')
print('запуск')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Инициализация альтернативной клавиатуры
    # TODO добавить one_time_keyboard=True в аргументы выше
    btn1 = types.KeyboardButton('Проверка ссылок') # Добавление кнопки
    btn2 = types.KeyboardButton('Справка по безопасности')
    btn3 = types.KeyboardButton('Генерация пароля')

    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nЯ - бот-киберпомощник, с чем требуется помощь?', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)

@bot.message_handler(commands=['help'])
def help_func(message):
    bot.send_message(message.chat.id, 'Тебе требуется помощь?!')

@bot.message_handler()
def info(message):
    if message.text == 'Справка по безопасности':
        bot.send_message(message.chat.id, 'Задай вопрос')
        bot.register_next_step_handler(message, topyc_sync)

    elif message.text.lower() in ('hello', 'привет'):
        bot.send_message(message.chat.id, 'Да привет, привет')
        # bot.reply_to(message, f'Да привет, привет')
        # start(message)
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}')
        # bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, f'Yupi Yo')
        # bot.reply_to(message, f'Yupi Yo')

def topyc_sync(message):
    actual_words = key_word_search(message.text)
    bot.send_message(message.chat.id, f'Всё что я понял:\n{actual_words}')

def on_click(message):
    bot.send_message(message.chat.id, f'{message.text}?')

bot.polling(none_stop=True)