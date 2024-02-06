import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

import sqlite3 as sql3


class Database:

    def __init__(self):
        self.db = sql3.connect("../../iubip.db")
        self.cursor = self.db.cursor()

        # Создание таблиц

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS reviews(
            user_id INT PRIMARY KEY,
            name_user TEXT,
            tg_id TEXT
            )"""
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS templates(
            user_id INT PRIMARY KEY,
            name_user TEXT,
            name_group TEXT
            tg_id TEXT
            )"""
        )
