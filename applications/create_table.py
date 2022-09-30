from applications.settings_path import DB_PATH
from connection_db import DBConnection


def create_table():
    with DBConnection(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                phone_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                contact_name TEXT NOT NULL,
                phone_value TEXT NOT NULL)
        ''')
