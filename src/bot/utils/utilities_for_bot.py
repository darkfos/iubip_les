from aiogram import types, Bot


async def set_commands_to_bot(iubip_bot: Bot) -> None:
    """
        Установка всех команд для description
    """
    
    all_commands = (
        types.BotCommand(command="start", description="Начало работы с ботом"),
        types.BotCommand(command="help", description="Поддержка, вывод списка команд"),
        types.BotCommand(command="all_lessons", description="Получение расписания на текущий день"),
        types.BotCommand(command="lessons_now", description="Получение расписания на текущий день"),
        types.BotCommand(command="all_groups", description="Получение списка всех учебных групп"),
    )

    await iubip_bot.set_my_commands(commands=all_commands)