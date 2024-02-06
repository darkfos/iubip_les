import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from aiogram.filters import BaseFilter
from aiogram import types

from src.database import db_templates as d_t


class CheckTemplates(BaseFilter):
    
    async def __call__(
            self,
            message: types.Message
    ):
        check_db = await d_t.get_temp(message.from_user.id)

        if check_db:
            await message.answer("🔴 <b>Внимание!</b> вы можете создать только 1 шаблон.\nВаш шаблон уже создан.", parse_mode="HTML")
            return False
        else: return True