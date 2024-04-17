import telebot
from telebot import types
from config.db_config import token
from funcs.db_funcs import DBConnection
from funcs.funcs import get_question, get_articles, get_password
from funcs.funcs import key_word_search
from markups import main_menu_markup, to_home_markup

bot = telebot.TeleBot(token)
connection = DBConnection()
print('запуск')


@bot.message_handler(commands=['start'])
def start(message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Инициализация альтернативной клавиатуры
    # # TODO добавить one_time_keyboard=True в аргументы выше
    # btn1 = types.KeyboardButton('Проверка ссылок') # Добавление кнопки
    # btn2 = types.KeyboardButton('Справка по безопасности')
    # btn3 = types.KeyboardButton('Генерация пароля')
    #
    # markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}!\nЯ - бот-киберпомощник, с чем требуется помощь?',
                     reply_markup=main_menu_markup)
    # bot.register_next_step_handler(message, on_click)

# @bot.message_handler(commands=['help'])
# def help_func(message):
#     bot.send_message(message.chat.id, 'Тебе требуется помощь?!')

@bot.message_handler()
def case_handling(message):
    if message.text == 'Справка по безопасности':
        bot.send_message(message.chat.id, 'Задайте вопрос', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, topyc_sync)
    elif message.text == 'Генерация пароля':
        bot.register_next_step_handler(message, passwords_handling)
    elif message.text.lower() in ('hello', 'привет'):
        bot.send_message(message.chat.id, 'Да привет, привет')
        # bot.reply_to(message, f'Да привет, привет')
        # start(message)
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}')
        # bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, f'Не знаю такого')
        # bot.reply_to(message, f'Yupi Yo')
    # types.ReplyKeyboardRemove(selective=False)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'wrong question':
        inl_keyb_reply = 'Переформулируйте вопрос, пожалуйста'
        bot.send_message(callback.message.chat.id, inl_keyb_reply)
        # bot.register_next_step_handler(callback, case_handling)
    elif callback.data == 'correct question':

        # prev_text = callback.message.text
        # bot.delete_message(callback.message.chat.id, message_id=callback.message.id)
        # bot.send_message(chat_id=callback.message.chat.id,text=prev_text)

        question = callback.message.text[18:-5]
        inl_keyb_reply = get_articles(question, connection)
        # inl_keyb_reply = db_connection.get_articles(connection, question)
        bot.send_message(callback.message.chat.id, inl_keyb_reply)

    elif 'password' in callback.data:
        inl_keyb_reply = get_password(callback.data)
        bot.send_message(callback.message.chat.id, inl_keyb_reply)

    else:
        inl_keyb_reply = 'пустота'
        bot.send_message(callback.message.chat.id, inl_keyb_reply)

    # bot.send_message(callback.message.chat.id, inl_keyb_reply)
    # print(f'1. {callback.message.chat.id = }')
    # bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.id, reply_markup=)  # удаляем кнопки у последнего сообщения
    # callback.message.update.callback_query.edit_message_reply_markup(None)



def topyc_sync(message):
    actual_words = key_word_search(message.text, connection)
    question = get_question(actual_words, connection)
    if question is None:
        bot.send_message(message.chat.id,f'Затрудняюсь ответить.\nПопробуйте переформулировать')
    else:
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn_yes = types.InlineKeyboardButton(text='Да',
                                             callback_data='correct question')
        btn_no = types.InlineKeyboardButton(text='Нет, другой вопрос',
                                            callback_data='wrong question')
        kb.add(btn_yes, btn_no)


        bot.send_message(message.chat.id,
                         f'Вы имели в виду \n"{question}"\n???',
                         reply_markup=kb)
        # print(f'1. {message.chat.id = }')
        # bot.send_message(message.chat.id, f'Акутальные слова:\n{actual_words}')
        # bot.send_message(message.chat.id, f'Таблица вопросов:\n{questions}')

def passwords_handling(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_easy = types.InlineKeyboardButton(text='Слабый пароль',
                                         callback_data='easy password')
    btn_medium = types.InlineKeyboardButton(text='Хороший пароль',
                                        callback_data='medium password')
    btn_hard = types.InlineKeyboardButton(text='Сложный пароль',
                                            callback_data='hard password')
    kb.add(btn_easy, btn_medium, btn_hard)

    bot.send_message(message.chat.id,
                     f'Какой пароль сгенерировать?',
                     reply_markup=kb)

def on_click(message):
    bot.send_message(message.chat.id, f'{message.text}?')

bot.polling(none_stop=True)