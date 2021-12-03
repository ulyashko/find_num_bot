import sqlite3


def search_by_db(num):
    sqlite_connection = sqlite3.connect('name_database.db')
    cursor = sqlite_connection.cursor()
    cursor.execute('SELECT bank FROM car_num WHERE num = ?', (num,))
    res = cursor.fetchone()

    return res