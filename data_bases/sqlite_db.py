import os
import sqlite3 as sq
import psycopg2 as ps
import os

from create_bot import bot


def sql_start():
    """Створення таблиці"""
    global base, curs
    # base = sq.connect('learn_words.db')
    base = ps.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    curs = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS words_to_study(id INTEGER, word TEXT)')
    base.commit()


def sql_save(data):
    """Збереження слова користувача в БД """
    curs.execute('INSERT INTO words_to_study VALUES(?, ?);', tuple(data.values()))
    base.commit()


async def sql_read(id):
    """Вивід слів користувача з БД"""
    my_words = []
    for word in curs.execute('SELECT word FROM words_to_study WHERE id == ?', (id,)).fetchall():
        my_words.append(word[0])
    await bot.send_message(id, '\n'.join(my_words))


def sql_check(data):
    """Перевірка, чи є слово в БД"""
    if curs.execute('SELECT word FROM words_to_study WHERE id == ? AND word == ?',
                    (data['id'], data['word'])).fetchall():
        return True


def sql_delete(data):
    """Видалення слова користувача з БД"""
    curs.execute('DELETE FROM words_to_study WHERE id == ? AND word == ?', (data['id'], data['word']))
    base.commit()


def sql_shutdown():
    """Безпечний вихід з БД"""
    curs.close()
    base.close()
