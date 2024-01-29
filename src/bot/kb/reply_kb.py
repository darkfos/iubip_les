from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from emoji import emojize


async def get_start_bt():
    """
        Возвращает кнопки для команды start
    """

    kb_start: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    kb_start.add(KeyboardButton(text=emojize(":books: Все пары"), language="en"))
    kb_start.add(KeyboardButton(text=emojize(":open_book: Пары на сегодня"), language="en"))

    return kb_start.as_markup()