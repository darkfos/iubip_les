import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from db import Database


db = Database()


async def get_all_reviews() -> list:
    all_reviews: list = db.cursor.execute("SELECT * FROM reviews")
    return all_reviews


async def get_reviews_by_tgid(tg_id: int) -> list | None:
    unique_review: list = db.cursor.execute(f"SELECT * FROM reviews WHERE tg_id == {tg_id}")
    if unique_review:
        return unique_review
    else: return None


async def add_review(**kwargs) -> bool:
    try:
        db.cursor.execute(f"INSERT INTO reviews VALUES ({kwargs.values()})")
        return True
    except ValueError:
        return False


async def del_review(tg_id: int) -> bool:
    try:
        db.cursor.execute(f"DELETE FROM reviews WHERE tg_id == {tg_id}")
        return True
    except ValueError:
        return False