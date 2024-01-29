import emoji

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def get_all_groups_bt() -> InlineKeyboardBuilder:
    bt = InlineKeyboardBuilder()
    bt.add(InlineKeyboardButton(text=emoji.emojize(":orange_book: Список", language="en"), callback_data="list_btn"))
    bt.add(InlineKeyboardButton(text=emoji.emojize(":green_book: CSV файл", language="en"), callback_data="csv_btn"))

    return bt.as_markup()

