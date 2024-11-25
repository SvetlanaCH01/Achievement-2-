import sqlite3

# создание таблицы
def create_database():
    conn = sqlite3.connect('numbers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_numbers (
            number INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

create_database()