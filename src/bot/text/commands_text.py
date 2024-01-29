

async def get_start_message(name_user: str) -> str:
    start_text: str = f"Привет {name_user}! Я бот который выводит расписание для учебного заведения <b>ИУБИП</b>\n\
Здесь ты можешь ознакомиться со всеми командами - <b>/help</b>"
    
    return start_text


async def get_help_commands() -> str:

    help_text: str = "<u>Мой перечень команд:</u>\n\n\
/start - Запуск бота\n\
/help - Функционал бота\n\
/all_lessons - Вывод всех пар по указанной группе\n\
/lessons_now - Вывод всех пар на текущий день\n\
/all_groups - Вывод всех учебных групп\n\
\nТак же ты можешь ввести название любой группы и получить полное расписание!"

    return help_text