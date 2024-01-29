from aiogram.filters import BaseFilter, StateFilter
from aiogram import types


class FilterAllGroups(BaseFilter):
    """
        Фильтр для получения формата списка групп
    """

    async def __call__(self, message: types.CallbackQuery) -> bool:
        if message.data in ("list_btn", "csv_btn"):
            return True
        else: return False