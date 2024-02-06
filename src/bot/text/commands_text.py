from emoji import emojize


async def get_start_message(name_user: str) -> str:
    start_text: str = f"Привет {name_user}! Я бот который выводит расписание для учебного заведения <b>ИУБИП</b>\n\
Здесь ты можешь ознакомиться со всеми командами - <b>/help</b>"
    
    return start_text


async def get_help_commands() -> str:

    help_text: str = "<u>Мой перечень команд:</u>\n\n\
🔔 <b>/start</b> - Запуск бота\n\
🔔 <b>/help</b> - Функционал бота\n\
🔔 <b>/all_lessons</b> - Вывод всех пар по указанной группе\n\
🔔 <b>/lessons_now</b> - Вывод всех пар на текущий день\n\
🔔 <b>/all_groups</b> - Вывод всех учебных групп\n\
🔔 <b>/cancel</b> - Отмена\n\
🔔 <b>/create_template</b> - Создание шаблона\n\
🔔 <b>/delete_template</b> - Удаление шаблона\n\
🔔 <b>/template</b> - Поиск по шаблону\n\
\n<i>Так же ты можешь ввести название любой группы и получить полное расписание!</i>"

    return help_text


text_to_all_groups = emojize(":bullseye: Пожалуйста выберите формат получения списка <b>всех</b> учебных групп", language="en")

text_cancel = emojize(":check_mark_button: Вы сбросили <b>все</b> процессы.")

text_to_find_group = emojize("⌨️ Пожалуйста введите вашу группу")