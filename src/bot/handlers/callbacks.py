import sys, os
import logging

#Установка локального пути
sys.path.insert(1, os.path.join(sys.path[0], "../.."))

#Aiogram
from aiogram import types, Router, F

#Сторонние библиотеки
from emoji import emojize

#Подключаем свои директивы
from src.bot.filters import all_groups_filter
from src.bot.utils.others import work_data
from src.bot.handlers.commands import get_all_lessons


#Роутер для обработки всех callbacks бота
callback_router: Router = Router()


@callback_router.callback_query(all_groups_filter.FilterAllGroups())
async def get_all_groups_file(callback_message: types.CallbackQuery) -> None:
    """
        Обработка нажатия на кнопку - список всех групп
    """

    #Если кнопка "Список"
    if callback_message.data == "list_btn":

        to_send_text: str = await work_data.get_list_all_groups()
        logging.info("Пользователь {0} выбрал список всех учебных групп.".format(callback_message.message.from_user.full_name))
        await callback_message.message.reply(text=emojize(f":books: <b>Список учебных групп:</b> \n\n{to_send_text}", language="en"), parse_mode="HTML")

    #CSV file
    else:
        
        logging.info("Пользователь {0} выбрал список всех учебных групп в формате csv.".format(callback_message.message.from_user.full_name))
        await callback_message.message.answer_document(document=await work_data.get_csv_all_groups())


@callback_router.message()
async def response_to_simple_message(message: types.Message):
    """
        Обработка всех лишних сообщений
    """
    await message.answer("Не могу распознать ваш текст, ожидаю команду или название группы")