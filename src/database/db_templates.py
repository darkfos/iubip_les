import sys, os
import sqlite3 as sql

import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from src.database.db import Database

db = Database()


async def get_temp(tg_id: int) -> str | bool:

    try:
        result: tuple = db.cursor.execute(f"""
        SELECT name_group FROM templates WHERE tg_id = {tg_id}
        """).fetchone()
        return result
    except sql.OperationalError:
        return False


async def post_temp(**kwargs) -> bool:
    try:
        answer = db.cursor.execute(f"""INSERT INTO templates (name_user, name_group, tg_id) VALUES (?, ?, ?)""", tuple(kwargs.values(),))
        db.db.commit()
        return True
    except sql.OperationalError:
        return False


async def del_temp(tg_id: int) -> bool:
    try:
        db.cursor.execute(f"""DELETE FROM templates WHERE tg_id == ({tg_id})""")
        db.db.commit()
        return True
    except sql.OperationalError:
        return False