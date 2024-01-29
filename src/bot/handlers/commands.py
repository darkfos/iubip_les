import sys, os
import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command


#Локальные директивы
from src.bot.text import commands_text
from src.bot.kb import inline_kb

commands_router = Router()


@commands_router.message(CommandStart())
async def start_bot(message: Message) -> None:
    """
        Стартовая команда бота.
    """

    #Картинка для отправки
    photo_to_send = FSInputFile("iubip_les/src/static/main_iubip.png")
    logging.info("Пользователь {} активировал команду start".format(message.from_user.full_name))
    await message.answer_photo(photo=photo_to_send, caption=await commands_text.get_start_message(message.from_user.full_name), parse_mode="HTML")


@commands_router.message(Command("help"))
async def help_commands(message: Message) -> None:

    """
        Команда для помощи.
    """
    logging.info("Пользователь {} активировал команду help".format(message.from_user.full_name))
    await message.answer(text=await commands_text.get_help_commands(), parse_mode="HTML")


@commands_router.message(Command("all_groups"))
async def all_groups_command(message: Message) -> None:
    await message.answer(text=commands_text.text_to_all_groups, parse_mode="HTML", reply_markup=await inline_kb.get_all_groups_bt())