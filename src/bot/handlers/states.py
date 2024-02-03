import sys, os
import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from src.bot.states.lessons_for_group import GetLessonsForGroup
from src.bot.filters import check_group_in_list

from src.parse_iubip.parse_lessons_for_group import Lessons
from src.parse_iubip.parse_all_groups import Groups

state_router: Router = Router()

@state_router.message(check_group_in_list.CheckGroup())
@state_router.message(GetLessonsForGroup.name_group)
async def write_all_lessons(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.full_name} сделал запрос на получение всех пар.")
    try:

        group_lessons: list = await Lessons(message.text).get_all_lessons_for_group()
        await message.answer(text="📖 Расписание <b>всех</b> пар", parse_mode="HTML")
        for lessons_day in group_lessons:
            await message.answer(text=lessons_day, parse_mode="HTML")
    except TypeError:
        await message.answer("К сожалению ваш запрос <u>не был обработан</u>", parse_mode="HTML")
