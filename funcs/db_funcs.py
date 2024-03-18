import psycopg2
from config.db_config import host, user, password, db_name, port

def db_open_connect():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        # cursor = connection.cursor()
        #
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         "select keyword from keywords;"
        #     )
        #     res = cursor.fetchall()
        #     key_word_list = []
        #     for key_word in res:
        #         key_word_list.append(str(key_word)[2:-3])

    except Exception as _ex:
        print(_ex)
    finally:
        if connection:
            return connection

def get_key_words(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "select keyword from keywords;"
        )
        res = cursor.fetchall()
        key_word_list = []
        for key_word in res:
            key_word_list.append(str(key_word)[2:-3])
    return key_word_list

def db_close_connection(connection):
    connection.close()