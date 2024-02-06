import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from db import Database

db = Database()


async def get_temp(tg_id: int) -> str | bool:
    result: tuple = db.cursor.execute(f"""
    SELECT name_group FROM templates WHERE tg_id == {tg_id}
    """)

    if result:
        return result[0]
    else:
        return False


async def post_temp(**kwargs) -> bool:
    try:
        db.cursor.execute(f"""INSERT INTO templates VALUES ({kwargs})""")
        return True
    except ValueError:
        return False


async def del_temp(tg_id: int) -> bool:
    try:
        db.cursor.execute(f"""DELETE FROM templates WHERE tg_id == ({tg_id})""")
        return True
    except ValueError:
        return False