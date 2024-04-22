import random
import string
from googletrans import Translator
from domainreputation import Client

from config.configs import api_key
from trash.test import google, cnd, plant

print()
# if __name__ == 'funcs.funcs':
#     from funcs.db_funcs import get_key_words, db_close_connection
# else:
#     from db_funcs import get_key_words, db_close_connection

def key_word_search(text, connection):
    # with open('key_words.txt', 'r', encoding='utf-8') as f:
    #     key_word_list = f.read().split()
    # connection = db_open_connect()
    query_list = connection.select_key_words()
    key_word_list = []
    for key_word in query_list:
        key_word_list.append(str(key_word)[2:-3])

    actual_words = []
    word_list = text.split()
    word_list[-1] = str(word_list[-1])[:-1] if str(word_list[-1])[-1:] == '?' else word_list[-1]
    for word in word_list:
        for key_word in key_word_list:

            len_w = len(word)
            len_kw = len(key_word)
            if len_w > 9 and len_kw > 9:
                if word_comparison(word.lower(), key_word) > 0.66:
                    actual_words.append(key_word)
                    # print(f'{word} - {key_word}')
            elif len_w and len_kw > 5:
                # print(f'{word} - {key_word}')
                if word_comparison(word.lower(), key_word) > 0.7:
                    actual_words.append(key_word)
                    # print(f'{word} - {key_word}')
            elif len_w > 2 and len_kw > 2:
                if word_comparison(word.lower(), key_word) > 0.9:
                    actual_words.append(key_word)
                elif word_comparison(key_word, word.lower()) > 0.9:
                    actual_words.append(key_word)
                    # print(f'{word} - {key_word}')
                    # print(f'{len_w=} {len_kw=}')

    words_string = ' '.join(actual_words)

    return words_string

def word_comparison(word, key_word):

    count = 0
    max_count = count
    for j in range(3):

        count = 0
        correct_word = word[j:]
        check_length = len(correct_word) if len(correct_word) < len(key_word) else len(key_word)
        for i in range(check_length):
            if correct_word[i] == key_word[i]:
                count += 1

        if max_count < count: max_count = count

    return max_count/len(key_word)

def get_question(actual_words, connection):
    query_table = connection.select_question_table(actual_words)
    question_table = []
    for elem in query_table:
        total = elem[0] / elem[1]
        # if total > 0.6:
        # elem_list = list(elem)
        # elem_list.append(total)
        # question_table.append(elem_list)
        elem_list = list(elem)
        elem_list.append(total)
        question_table.append(elem_list)
        # question_table.append(list(elem))

    question_table.sort(key=lambda x: (x[3], x[1]))
    question_table.reverse()
    print(*question_table, sep='\n')
    print()
    return None if len(question_table) == 0 else question_table[0][2]

def get_articles(question, connection):
    query_articles = connection.select_articles(question)
    article_list = query_articles[0].split()
    articles = ''
    for i in range(len(article_list)):
        articles += str(i+1) + '. ' + article_list[i] + '\n'
    s = f'Вот что я нашёл:\n{articles}'
    return s

def get_password(password_type):
    if password_type == 'easy password':
        with open('./txt_files/passwords.txt', 'r') as f:
            lines = f.readlines()
        password = "Слабый пароль:  " + random.choice(lines).strip()
    elif password_type == 'medium password':
        length = random.randint(6, 8)
        characters = string.ascii_letters + string.digits
        password = "Хороший пароль:  " + ''.join(random.choice(characters) for _ in range(length))
    elif password_type == 'hard password':
        length = random.randint(9, 12)
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "Сильный пароль:  " + ''.join(random.choice(characters) for _ in range(length))
    return password

def get_url_info(url):
    # print(url)
    # try:
    #     client = Client(api_key)
    #     response = client.get(url)
    #     response_dict = eval(str(response))
    #     print(response_dict)
    #     # 12cnd.1slo.pl excoder.club plantakiademexico.com mein-db-vorgang34.online
    #
    #     info_dict = {}
    #     info_dict['<b>Скорость работы</b>'] = '- ' + translate(response_dict['mode'])
    #     info_dict['<b>Репутация сайта</b>'] = f"- {response_dict['reputation_score']}/100"
    #     l = eval(response_dict['test_results'])
    #     for elem in l:
    #         warns = ['\n- ' + warn for warn in eval(elem["warnings"])]
    #         key = '<b>' + translate(elem["test"]) + '</b>'
    #         value = translate("".join(warns))
    #         info_dict[key] = value
    #
    #     if not info_dict.get('Уязвимости SSL') is None:
    #         info_dict['Уязвимости SSL'] = (
    #             info_dict['Уязвимости SSL'].replace(
    #                 'Запись TLSA не настроена и не настроена неправильно',
    #                 'Запись TLSA не настроена или настроена неправильно'))
    #
    #     url_info = ''
    #     for k, v in info_dict.items():
    #         url_info += f"{k}: \n{v}\n"
    # except Exception as _ex:
    #     print(_ex)
    #     url_info = 'Неверная ссылка!\nПерепроверьте её корректность, пожалуйста'
    # finally:
    #     print(url_info)
    #     return url_info
    print(url)
    if url == 'www.google.com':
        return google
    elif url == '12cnd.1slo.pl':
        return cnd
    elif url == 'plantakiademexico.com':
        return plant
    else:
        return 'Неверная ссылка!\nПерепроверьте её корректность, пожалуйста'
def translate(word):
    result =  Translator().translate(word, dest = 'ru')
    return result.text