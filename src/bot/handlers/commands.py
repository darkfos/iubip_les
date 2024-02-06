import sys, os
import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


#Локальные директивы
from src.bot.text import commands_text
from src.bot.kb import inline_kb, reply_kb
from src.bot.states import lessons_for_group, work_with_db as wwd
from src.parse_iubip import parse_lessons_for_group
#БД
from src.database import db_templates as db_t, db_reviews as db_r

commands_router = Router()


@commands_router.message(CommandStart())
async def start_bot(message: Message) -> None:
    """
        Стартовая команда бота.
    """

    #Картинка для отправки
    photo_to_send = FSInputFile("iubip_les/src/static/main_iubip.png")
    logging.info("Пользователь {} активировал команду start".format(message.from_user.full_name))
    await message.answer_photo(photo=photo_to_send, caption=await commands_text.get_start_message(message.from_user.full_name), parse_mode="HTML", reply_markup=await reply_kb.get_start_bt())


@commands_router.message(Command("help"))
async def help_commands(message: Message) -> None:
    """
        Команда для помощи.
    """
    photo_to_send = FSInputFile("iubip_les/src/static/help_photo.jpg")
    logging.info("Пользователь {} активировал команду help".format(message.from_user.full_name))
    await message.answer_photo(photo=photo_to_send, caption=await commands_text.get_help_commands(), parse_mode="HTML")


@commands_router.message(Command("all_groups"))
async def all_groups_command(message: Message) -> None:
    """
        Команда для получения списка учебных групп.
    """

    logging.info("Пользователь {} активировал команду all_groups ожидается выбор формата ответа".format(message.from_user.full_name))
    await message.answer(text=commands_text.text_to_all_groups, parse_mode="HTML", reply_markup=await inline_kb.get_all_groups_bt())


@commands_router.message(lambda message: message.text[2:].lower() in "все пары")
@commands_router.message(Command("all_lessons"))    
async def get_all_lessons(message: Message, state: FSMContext):
    logging.info("Обработка, получение всех пар")
    await state.set_state(lessons_for_group.GetLessonsForGroup.name_group)
    await message.answer(text=commands_text.text_to_find_group)


@commands_router.message(lambda message: message.text[2:].lower() in "пары на сегодня")
@commands_router.message(Command("lessons_now"))
async def command_lessons_now(message: Message, state: FSMContext):
    await state.set_state(lessons_for_group.GetLessonsNow.name_group)
    await message.answer(text=commands_text.text_to_find_group)


@commands_router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext) -> None:
    """
        Команда для отмены FSM - Finite State Machine
    """

    logging.critical("Пользователь {} сбросил состояния.".format(message.from_user.full_name))

    #Очистка состояния
    await state.clear()

    await message.answer(text=commands_text.text_cancel, parse_mode="HTML")


#Работа с шаблонами
    
@commands_router.message(Command("create_template"))
async def create_template(message: Message, state: FSMContext):
    await message.answer("💥 Хорошо, {0} давай создадим тебе шаблон для поиска. Не забудь его можно удалить с помощью команды <b>/delete_template</b> !".format(message.from_user.full_name), parse_mode="HTML")
    await state.set_state(wwd.CreateTemplate.name_group)
    await message.answer("🖍️ Введи название своей группы")


@commands_router.message(Command("delete_template"))
async def delete_template(message: Message):
    await message.answer("💥 Вы выбрали удалить шаблон, ожидайте, операция выполняется")
    result = await db_t.del_temp(message.from_user.id)
    if result:
        await message.answer("💥 Ваш шаблон <b>был успешно удалён</b>", parse_mode="HTML")
    else: await message.answer("🔴 <b>Шаблон не был удалён</b>, возможно вы его ещё не создали", parse_mode="HTML")


@commands_router.message(Command("template"))
async def get_lessons_for_template(message: Message):
    result = await db_t.get_temp(message.from_user.id)

    if result:
        lessons_object = lessons_for_group.Lessons(result[0])

        message: list = await lessons_object.parse_lessons_for_group()

        for lesson in message:
            await message.answer(text=lesson, parse_mode="HTML")
    
    else:

        await message.answer(text="🔴 Не могу выполнить данную команду")
