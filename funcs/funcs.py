from db_funcs import db_open_connect, get_key_words, db_close_connection


def key_word_search(text):
    # with open('key_words.txt', 'r', encoding='utf-8') as f:
    #     key_word_list = f.read().split()
    connection = db_open_connect()
    key_word_list = get_key_words(connection)
    db_close_connection(connection)

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

        # if len(correct_word) < len(key_word):
        #     check_length = len(correct_word)
        #     compare_length = len(key_word)
        # else:
        #     check_length = len(key_word)
        #     compare_length = len(correct_word)
        check_length = len(correct_word) if len(correct_word) < len(key_word) else len(key_word)
        for i in range(check_length):
            if correct_word[i] == key_word[i]:
                count += 1

        if max_count < count: max_count = count

    return max_count/len(key_word)

