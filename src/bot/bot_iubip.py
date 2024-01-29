import sys, os
import logging

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from read_information import TOKEN


async def start_bot():
    Bot_iubip = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp_bot = Dispatcher(bot=Bot_iubip, storage=storage)
    logging.basicConfig(level=logging.INFO)

    await dp_bot.start_polling(Bot_iubip)