import asyncio
import os, sys

from src.bot import bot_iubip

if __name__ == "__main__":
    #Запуск Бота
    asyncio.run(bot_iubip.start_bot())