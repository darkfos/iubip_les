import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram.filters import BaseFilter, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types

from src.parse_iubip.parse_all_groups import Groups


class CheckGroup(BaseFilter):

    async def __call__(
            self,
            message: types.Message,
    ):
        all_groups: list = await Groups().get_all_groups()

        for group in all_groups:
            if message.text in group:
                return True
        else:
            await message.answer("🔴 Данной группы не существует")
            return False