import sys, os
import logging

#Устанавливаем локальный путь
sys.path.insert(1, os.path.join(sys.path[0], "../.."))

#Aiogram
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext


#Импорт сторонних библиотек
from datetime import datetime
from emoji import emojize


#Локальные директивы
from src.bot.text import commands_text
from src.bot.kb import inline_kb, reply_kb
from src.bot.states import lessons_for_group, work_with_db as wwd, reviews as rev
from src.parse_iubip.parse_lessons_for_group import Lessons


#БД
from src.database import db_templates as db_t, db_reviews as db_r

#Роутер, обработка команд бота
commands_router = Router()


@commands_router.message(CommandStart())
async def start_bot(message: Message) -> None:
    """
        Стартовая команда бота.
    """

    #Картинка для отправки
    photo_to_send = FSInputFile("src/static/main_iubip.png")
    logging.info("Пользователь {} активировал команду start".format(message.from_user.full_name))
    await message.answer_photo(photo=photo_to_send, caption=await commands_text.get_start_message(message.from_user.full_name), parse_mode="HTML", reply_markup=await reply_kb.get_start_bt())


@commands_router.message(Command("help"))
async def help_commands(message: Message) -> None:
    """
        Команда для помощи.
    """
    photo_to_send = FSInputFile("src/static/help_photo.jpg")
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
    """
        Пользователь получает список всех имеющихся пар
    """
    logging.info("Обработка, получение всех пар")
    await state.set_state(lessons_for_group.GetLessonsForGroup.name_group)
    await message.answer(text=commands_text.text_to_find_group)


@commands_router.message(lambda message: message.text[2:].lower() in "пары на сегодня")
@commands_router.message(Command("lessons_now"))
async def command_lessons_now(message: Message, state: FSMContext) -> None:
    """
        Пользователь получает список всех пар на текущий день
    """
    logging.info("Обработка команды 'пары на сегодня'")
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
async def create_template(message: Message, state: FSMContext) -> None:
    """
        Создание шаблона по команде create_template
    """
    await message.answer("💥 Хорошо, {0} давай создадим тебе шаблон для поиска. Не забудь его можно удалить с помощью команды <b>/delete_template</b> !".format(message.from_user.full_name), parse_mode="HTML")
    await state.set_state(wwd.CreateTemplate.name_group)
    logging.info("Пользователь {} создает свой шаблон, ввод названия группы".format(message.from_user.full_name))
    await message.answer("🖍️ Введи название своей группы")


@commands_router.message(Command("delete_template"))
async def delete_template(message: Message) -> None:
    """
        Удаляем шаблон по команде - delete_templates
    """
    await message.answer("💥 Вы выбрали удалить шаблон, ожидайте, операция выполняется")
    result = await db_t.del_temp(message.from_user.id)
    if result:
        await message.answer("💥 Ваш шаблон <b>был успешно удалён</b>", parse_mode="HTML")
        logging.info("Пользователь {} удалил свой шаблон".format(message.from_user.full_name))
    else: await message.answer("🔴 <b>Шаблон не был удалён</b>, возможно вы его ещё не создали", parse_mode="HTML")


@commands_router.message(Command("template"))
async def get_lessons_for_template(message: Message) -> None:
    """
        Обработка шаблона, вывод списка пар на 3 дня.
    """
    
    logging.info("Пользователь {0} вызвал шаблон для получения расписания на 3 дня".format(message.from_user.full_name))
    result = await db_t.get_temp(message.from_user.id)
    if result:
        lessons_object = Lessons(result[0])

        message_to_user: list = await lessons_object.get_lessons_for_3d()
        await message.answer(text="💤 Ожидайте операция выполняется")

        all_less: list = list()

        if message_to_user:

            indx_week_days: int = 0    
            str_to_append: str = ""
            for message_lessons in message_to_user[0]:                
                if message_lessons != "\n\n":
                    str_to_append += message_lessons
                
                else:

                    all_less.append(f"<b><i>День недели: {message_to_user[1][indx_week_days]}</i></b>\n\n" + str_to_append)

                    indx_week_days += 1

                    str_to_append = ""

            
            for lessons in all_less:
                
                await message.answer(text=lessons, parse_mode="HTML")

        else:

            await message.answer(text="🔴 Занятий нет")
    
    else:

        await message.answer(text="🔴 Не могу выполнить данную команду")




# Работа с отзывами
@commands_router.message(Command("review"))
async def review_user(message: Message, state: FSMContext) -> None:
    """
        Обработка команды 'review', получаем состояние review
    """
    await message.answer(text=emojize(":check_mark: Введите ваше <b>имя</b>", language="en"), parse_mode="HTML")
    await state.set_state(rev.ReviewUser.name_user)
