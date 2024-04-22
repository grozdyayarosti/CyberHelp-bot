import time
import telebot
from telebot import types
from config.configs import token
from funcs.db_funcs import DBConnection
from funcs.funcs import get_question, get_articles, get_password, get_url_info
from funcs.funcs import key_word_search
from markups import main_menu_markup, to_home_markup, to_home_btn

bot = telebot.TeleBot(token)
connection = DBConnection()
print('запуск')

##########################################################################################
#  ОБРАБОТЧИК КОМАНД                                                                     #
##########################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.first_name if message.from_user.is_bot else message.from_user.first_name
    bot.send_message(message.chat.id,
                     f'Привет, {user}!\nЯ бот-киберпомощник, с чем требуется помощь?',
                     reply_markup=main_menu_markup)

##########################################################################################
#  ОБРАБОТЧИК ГЛАВНОГО МЕНЮ                                                              #
##########################################################################################
@bot.message_handler()
def case_handling(message):
    if message.text == 'Проверка ссылок':
        delete_ReplyKeyboard(message)
        bot.send_message(message.chat.id, 'Отправьте ссылку, я её проверю', reply_markup=to_home_markup)
        bot.register_next_step_handler(message, url_checking)
    elif message.text == 'Справка по безопасности':
        delete_ReplyKeyboard(message)
        bot.send_message(message.chat.id, 'Задайте вопрос', reply_markup=to_home_markup)
        bot.register_next_step_handler(message, topyc_synchronization)
    elif message.text == 'Генерация пароля':
        passwords_handling(message)
    # elif message.text.lower() in ('hello', 'привет'):
    #     bot.send_message(message.chat.id, 'Да привет, привет')
    #     # bot.reply_to(message, f'Да привет, привет')
    #     # start(message)
    # elif message.text.lower() == 'id':
    #     bot.send_message(message.chat.id, f'ID: {message.from_user.id}')
    #     # bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, f'Выберите опцию меню')

##########################################################################################
#  ОБРАБОТЧИК callback                                                                   #
##########################################################################################
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'wrong question':
        delete_ReplyKeyboard(callback.message)
        bot.send_message(callback.message.chat.id, 'Переформулируйте вопрос, пожалуйста', reply_markup=to_home_markup)
        bot.register_next_step_handler(callback.message, topyc_synchronization)
    elif callback.data == 'correct question':
        question = callback.message.text[18:-5]
        inl_keyb_reply = get_articles(question, connection)
        bot.send_message(callback.message.chat.id, inl_keyb_reply, reply_markup=main_menu_markup)

    elif 'password' in callback.data:
        inl_keyb_reply = get_password(callback.data)
        bot.send_message(callback.message.chat.id, inl_keyb_reply, reply_markup=main_menu_markup)

    elif callback.data == 'to home':
        bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        start(callback.message)

    else:
        bot.send_message(callback.message.chat.id, 'пустота')

##########################################################################################
#  ФУНКЦИИ ДЛЯ ОБРАБОТЧИКОВ                                                              #
##########################################################################################
def url_checking(message):
    url = message.text
    url = url.split('/')[2] if url[:4] == 'http' else url.split('/')[0]
    wait_message = bot.send_message(
        message.chat.id,
        "Я изучаю ссылку.\nПожалуйста, подождите . . . ",
        parse_mode='HTML')
    time.sleep(3)
    output = get_url_info(url)
    print(f'{output = }')
    bot.delete_message(message.chat.id, wait_message.id)
    bot.send_message(message.chat.id, output, parse_mode='HTML', reply_markup=main_menu_markup)

def topyc_synchronization(message):
    actual_words = key_word_search(message.text, connection)
    question = get_question(actual_words, connection)
    # print(f'{actual_words = }')
    # print(f'{question = }')
    if question is None:
        bot.send_message(message.chat.id,
                         f'Затрудняюсь ответить.\nПопробуйте переформулировать',
                         reply_markup=to_home_markup)
        bot.register_next_step_handler(message, topyc_synchronization)
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
        # bot.send_message(message.chat.id, f'Акутальные слова:\n{actual_words}')
        # bot.send_message(message.chat.id, f'Таблица вопросов:\n{questions}')

def passwords_handling(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_easy = types.InlineKeyboardButton(text='Слабый пароль',
                                         callback_data='easy password')
    btn_medium = types.InlineKeyboardButton(text='Хороший пароль',
                                        callback_data='medium password')
    btn_hard = types.InlineKeyboardButton(text='Сильный пароль',
                                            callback_data='hard password')
    kb.add(btn_easy, btn_medium, btn_hard)

    delete_ReplyKeyboard(message)
    bot.send_message(message.chat.id,
                     f'Какой пароль сгенерировать?',
                     reply_markup=kb)

def on_click(message):
    bot.send_message(message.chat.id, f'{message.text}?')

def delete_ReplyKeyboard(msg):
    delete_keyboard_msg = bot.send_message(msg.chat.id, 'Пожалуйста, подождите . . . ',
                                           reply_markup=types.ReplyKeyboardRemove())
    time.sleep(0.5)
    bot.delete_message(msg.chat.id, delete_keyboard_msg.id)

bot.polling(none_stop=True)