import sys, os
import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram import types, Router
from aiogram.fsm.context import FSMContext

#Локальные директивы
from src.bot.states.lessons_for_group import GetLessonsForGroup, GetLessonsNow
from src.bot.states.work_with_db import CreateTemplate, CreateReview
from src.bot.filters import check_group_in_list, check_templates

from src.parse_iubip.parse_lessons_for_group import Lessons
from src.parse_iubip.parse_all_groups import Groups

#БД
from src.database import db_reviews, db_templates

state_router: Router = Router()


@state_router.message(GetLessonsForGroup.name_group)
async def write_all_lessons(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.full_name} сделал запрос на получение всех пар.")
    all_groups: list = await Groups().get_all_groups()

    name_group: str = ""
    for group in all_groups:
        if message.text in group:
            name_group = group
            break
    
    if name_group != "":
        try:
                
            group_lessons: list = await Lessons(name_group).get_all_lessons_for_group()
            await message.answer(text="📖 Расписание <b>всех</b> пар", parse_mode="HTML")
            for lessons_day in group_lessons:
                await message.answer(text=lessons_day, parse_mode="HTML")

            logging.debug("Состояние имени группы было очищено")
            await state.clear()

        except TypeError:
            await message.answer(text="К сожалению ваш запрос <u>не был обработан</u>", parse_mode="HTML")

    else:
        await message.answer(text="Группа не была найдена, попробуйте ещё раз.")

    
@state_router.message(GetLessonsNow.name_group)
async def get_lessons_now(message: types.Message, state: FSMContext):
    logging.info(f"Пользователь {message.from_user.full_name} сделал запрос на получение пар на текущий день.")
    all_groups: list = await Groups().get_all_groups()

    name_group: str = ""
    for group in all_groups:
        if message.text in group:
            name_group = group
            break
    
    if name_group != "":
        lessons_for_now: list | bool = await Lessons(name_group).get_now_lessons()

        if lessons_for_now:

            message_to_user: str = "".join(lessons_for_now)
            await message.answer(text=message_to_user, parse_mode="HTML")
            await state.clear()
        
        else:

            await message.answer(text="📕 На сегодня пар нет")
            await state.clear()

    else:
        await message.answer(text="Группа не была найдена, попробуйте ещё раз.")


#Обработка создания шаблона
@state_router.message(CreateTemplate.name_group, check_group_in_list.CheckGroup(), check_templates.CheckTemplates())
async def create_template(message: types.Message, state: FSMContext):
    all_groups: list = await Groups().get_all_groups()
    message_to_res = message.text

    for group in all_groups:
        if message_to_res in group:
            message_to_res = group

    await state.update_data(name_group = message_to_res)
    all_data = await state.get_data()
    await state.clear()
    db_tmp = await db_templates.post_temp(name_user=message.from_user.full_name, name_group=all_data.get("name_group"), tg_id=message.from_user.id)

    if db_tmp:
        await message.answer("💥 Ваш шаблон был успешно создан")
    else:
        await message.answer("🔴 К сожалению ваш шаблон не был создан.")
