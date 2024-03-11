text = "TCP/IP"

def key_word_search(text):
    with open('../key_words.txt', 'r', encoding='utf-8') as f:
        key_word_list = f.read().split()
    actual_words = []
    word_list = text.split()
    for word in word_list:
        for key_word in key_word_list:
            print(f'key_word - {key_word}')
            if word_comparison(word.lower(), key_word) > 0.6:
                actual_words.append(key_word)
                # print(f'key_word - {key_word}')
    words_string = ' '.join(actual_words)

    return words_string
def word_comparison(word, key_word):

    count = 0
    max_count = 0
    for j in range(3):

        count = 0
        correct_word = word[j:]
        check_length = len(correct_word) if len(correct_word) < len(key_word) else len(key_word)
        for i in range(check_length):
            # print(f'\n{correct_word}')
            if correct_word[i] == key_word[i]:
                count += 1
                # print(correct_word[i])

        if max_count < count: max_count = count
    # print(max_count/len(key_word))
    return max_count/len(key_word)

a = key_word_search(text)
# a = word_comparison(text, 'TCP/IP')
print(a)