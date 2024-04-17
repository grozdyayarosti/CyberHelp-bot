import psycopg2
from config.db_config import host, user, password, db_name, port

class DBConnection:
    def __init__(self):
        self.connection = None
    def open_connection(self):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port
            )
        except Exception as _ex:
            print(_ex)
    def close_connection(self):
        self.connection.close()
    def db_cursor(self):
        return self.connection.cursor()

    def select_key_words(self):
        self.open_connection()
        with self.db_cursor() as cursor:
            cursor.execute(
                "select keyword from keywords;"
            )
            res = cursor.fetchall()
        self.close_connection()
        return res

    def select_question_table(self, actual_words):
        words_list = actual_words.split()
        if len(words_list) != 0:
            self.open_connection()
            with self.db_cursor() as cursor:
                cursor.execute(
                    f"select * "
                    "from "
                    f"get_words_questions(ARRAY {actual_words.split()});"
                )
                res = cursor.fetchall()
            self.close_connection()
        else:
            res = []
        return res

    def select_articles(self, question):
        print(f'{question = }\n')
        self.open_connection()
        with self.db_cursor() as cursor:
            cursor.execute(
                f"select distinct article "
                f"from articles "
                f"where question = '{question}'"
            )
            res = cursor.fetchone()
        self.close_connection()
        return res
