import asyncio
import logging

from src.bot import bot_iubip

if __name__ == "__main__":
    
    #Запуск Бота
    try:

        asyncio.run(bot_iubip.start_bot())

    except KeyboardInterrupt:
        logging.exception("Бот завершил свою работу")