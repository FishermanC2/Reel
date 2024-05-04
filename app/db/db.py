import sqlite3
import logging
from helper.singleton import Singleton


class HookDB(metaclass=Singleton):
    def __init__(self):
        self._conn = sqlite3.connect('app/db/hooks.db', check_same_thread=False)
        self._cursor = self._conn.cursor()

        try:
            self._cursor.execute(''' 
CREATE TABLE Hooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        ''')
        except sqlite3.OperationalError:
            logging.info("Table already exists")
        finally:
            logging.info("Hooks table created")

    def __del__(self):
        if self._conn:
            self._conn.close()

    def register_hook(self) -> int:
        self._cursor.execute('''
INSERT INTO Hooks DEFAULT VALUES
        ''')
        self._conn.commit()
        logging.info(f"Hook {self._cursor.lastrowid} created. ")
        return self._cursor.lastrowid
