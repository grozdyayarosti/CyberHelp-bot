from funcs import key_word_search, word_comparison

# text = "TCP/IP"
print()
# def key_word_search(text):
#     with open('../key_words.txt', 'r', encoding='utf-8') as f:
#         key_word_list = f.read().split()
#     actual_words = []
#     word_list = text.split()
#     for word in word_list:
#         for key_word in key_word_list:
#             # print(f'key_word - {key_word}')
#             if word_comparison(word.lower(), key_word) > 0.6:
#                 actual_words.append(key_word)
#                 # print(f'key_word - {key_word}')
#     words_string = ' '.join(actual_words)
#
#     return words_string
# def word_comparison(word, key_word):
#
#     count = 0
#     max_count = 0
#     for j in range(3):
#
#         count = 0
#         correct_word = word[j:]
#         check_length = len(correct_word) if len(correct_word) < len(key_word) else len(key_word)
#         for i in range(check_length):
#             # print(f'\n{correct_word}')
#             if correct_word[i] == key_word[i]:
#                 count += 1
#                 # print(correct_word[i])
#
#         if max_count < count: max_count = count
#     # print(max_count/len(key_word))
#     return max_count/len(key_word)

# a = key_word_search(question)
# a = word_comparison(text, 'TCP/IP')
def get_insert_query():
    with open('../txt_files/key_words.txt', 'r', encoding='utf-8') as f_r:
        key_word_list = f_r.read().split()
        with open('../txt_files/query.txt', 'w', encoding='utf-8') as f_w:
            for word in key_word_list:
                f_w.write(f"insert into keywords(keyword) values('{word}');\n")
def get_kw_list(question):
    a = key_word_search(question)
    with open('../txt_files/keywords_for_question.txt', 'w', encoding='utf-8') as f_w:
        # f_w.write('[')
        kw_list = a.split()
        s = '['
        for word in kw_list:
            s += f"'{word}', "
            # print(word)
        s = s[:-2] + ']'
        f_w.write(s)
        print(s)
    return s
    # print(word_comparison('системе', 'стек'))

# question = 'Какие уязвимости могут быть обнаружены в моей информационной системе?'
# question = 'Какие методы аутентификации являются наиболее безопасными?'
# question = 'Какие риски связаны с использованием общедоступных Wi-Fi сетей?'
# question = 'Какой антивирус выбрать для домашнего компьютера?'
# question = 'Что такое информационная безопасность?'
# question = 'Какие уязвимости могут существовать в мобильных приложениях?'
# question = 'Какие виды атак на веб-приложения существуют?'
# question = 'Какие основные принципы безопасного использования паролей?'
# question = 'Какие меры безопасности можно применить для защиты своего домашнего Wi-Fi роутера?'
question = 'Какие существуют методы обнаружения и предотвращения атак на информационную безопасность?'
get_kw_list(question)
# get_insert_query()

# print(word_comparison('атак', 'атака'))
# print(word_comparison('атака', 'атак'))