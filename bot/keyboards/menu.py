from aiogram.types import BotCommand
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats

from bot.bot_module import bot

async def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/ticket <ticket_id> <msg>',
                description='Отправка сообщения в тикет под определенным id'),
        BotCommand(command='/took <ticket_id>',
                description='Взять свободный тикет'),
        BotCommand(command='/tickets',
                description='Посмотреть все свободные тикеты')
        ]

    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeAllPrivateChats())