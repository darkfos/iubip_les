from aiogram.fsm.state import State, StatesGroup


class CreateTemplate(StatesGroup):
    name_group: str = State()


class CreateReview(StatesGroup):
    review_message: str = State()