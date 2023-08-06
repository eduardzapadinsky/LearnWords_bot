import sqlite3 as sq

from create_bot import bot


def sql_start():
    """
    Create a table in the database.
    This function establishes a connection to the database and creates a table called 'words_to_study'
    if it does not exist already. The table has two columns, 'id' of type INTEGER and 'word' of type TEXT.
    Returns:
        None
    """

    global base, curs
    base = sq.connect('learn_words.db')
    curs = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS words_to_study(id INTEGER, word TEXT)')
    base.commit()


def sql_save(data):
    """
    Save a user's word in the database.
    Args:
        data (dict): A dictionary containing 'id' and 'word' keys representing user ID and word to save.
    Returns:
        None
    """

    curs.execute('INSERT INTO words_to_study VALUES(?, ?);', tuple(data.values()))
    base.commit()


async def sql_read(id):
    """
    Retrieve user's words from the database and send them as a message.
    Args:
        id (int): The user's ID.
    Returns:
        None
    """
    my_words = []
    for word in curs.execute('SELECT word FROM words_to_study WHERE id == ?', (id,)).fetchall():
        my_words.append(word[0])
    await bot.send_message(id, '\n'.join(my_words))


def sql_check(data):
    """
    Check if a word exists in the database for a specific user.
    Args:
        data (dict): A dictionary containing 'id' and 'word' keys representing user ID and word to check.
    Returns:
        bool: True if the word exists in the database for the specified user, False otherwise.
    """

    if curs.execute('SELECT word FROM words_to_study WHERE id == ? AND word == ?',
                    (data['id'], data['word'])).fetchall():
        return True


def sql_delete(data):
    """
    Delete a user's word from the database.
    Args:
        data (dict): A dictionary containing 'id' and 'word' keys representing user ID and word to delete.
    Returns:
        None
    """

    curs.execute('DELETE FROM words_to_study WHERE id == ? AND word == ?', (data['id'], data['word']))
    base.commit()
