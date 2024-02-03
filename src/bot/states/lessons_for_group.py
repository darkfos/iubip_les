from aiogram.fsm.state import State, StatesGroup


class GetLessonsForGroup(StatesGroup):
    """
        Состояние - получение названия группы
    """

    name_group: str = State()
