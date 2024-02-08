import sys, os
import sqlite3 as sql

import logging

#Установка локального пути
sys.path.insert(1, os.path.join(sys.path[0], "../.."))

#Подключение директивы БД
from src.database.db import Database

#Инициализация БД
db = Database()


async def get_all_reviews() -> list:
    """
        Асинхронный метод для получения всех отзывов
    """

    all_reviews: list = db.cursor.execute("SELECT * FROM reviews")
    logging.info("Был осуществлён процесс получения всех отзывов")
    return all_reviews


async def get_reviews_by_tgid(tg_id: int) -> list | None:
    """
        Асинхронный метод для получения отзыва по tg_id
    """

    unique_review: list = db.cursor.execute(f"SELECT * FROM reviews WHERE tg_id = {tg_id}").fetchone()
    logging.info("Был осуществлён процесс получения всех отзывов по tg_id")
    if unique_review:
        return unique_review
    else: return None


async def add_review(**kwargs) -> bool:
    """
        Асинхронный метод для добавления отзыва
    """

    try:

        db.cursor.execute(f"INSERT INTO reviews (name_user, message, date, tg_id) VALUES (?, ?, ?, ?)", tuple(kwargs.values(),))
        logging.info("Был осуществлён процесс добавления отзыва")
        db.db.commit()
        return True
    
    except sql.OperationalError:
        return False


async def del_review(tg_id: int) -> bool:
    """
        Асинхронный метод для удаления отзыва
    """

    try:

        db.cursor.execute(f"DELETE FROM reviews WHERE tg_id == {tg_id}")
        logging.info("Был осуществлён процесс удаления отзыва")
        db.db.commit()
        return True
    
    except sql.OperationalError:
        return False