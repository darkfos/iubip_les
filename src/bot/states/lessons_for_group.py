from aiogram.fsm.state import State, StatesGroup


class GetLessonsForGroup(StatesGroup):
    """
        Состояние - получение названия группы, для расписания всех пар
    """

    name_group: str = State()


class GetLessonsNow(StatesGroup):
    """
        Состояние - получение названия группы, для расписания пар на текущий день
    """

    name_group: str = State()
