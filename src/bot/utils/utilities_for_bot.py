from aiogram import types, Bot


async def set_commands_to_bot(iubip_bot: Bot) -> None:
    """
        Установка всех команд для description
    """
    
    all_commands = (
        types.BotCommand(command="start", description="💥 Начало работы с ботом"),
        types.BotCommand(command="help", description="💥 Поддержка, вывод списка команд"),
        types.BotCommand(command="all_lessons", description="💥 Получение расписания всех пар"),
        types.BotCommand(command="lessons_now", description="💥 Получение расписания на текущий день"),
        types.BotCommand(command="all_groups", description="💥 Получение списка всех учебных групп"),
        types.BotCommand(command="create_template", description="💥 Создание шаблона"),
        types.BotCommand(command="delete_template", description="💥 Удаление шаблона"),
        types.BotCommand(command="template", description="💥 Поиск по шаблону"),
        types.BotCommand(command="review", description="💥 Оставить отзыв"),
        types.BotCommand(command="cancel", description="💥 Отмена")
    )

    await iubip_bot.set_my_commands(commands=all_commands)