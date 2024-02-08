from datetime import datetime
from aiogram.fsm.state import StatesGroup, State


class ReviewUser(StatesGroup):
    """
        Состояние для получения отзыва от пользователя.

        Имя
        Сообщение
        Дата

        Записывается в БД, таблица reviews
    """

    name_user: str = State()
    message_user: str = State()
    date_message_from_user: datetime