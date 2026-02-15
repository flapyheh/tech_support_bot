from aiogram import Bot
from aiogram.types import BotCommand

from bot.enums.enums import Sender

async def set_main_menu(bot: Bot, sender: Sender):
    main_menu_commands = [
        BotCommand(command='/ticket <ticket_id> <msg>',
                description='Отправка сообщения в тикет под определенным id'),
        BotCommand(command='/took <ticket_id>',
                description='Взять свободный тикет'),
        BotCommand(command='/tickets',
                description='Посмотреть все свободные тикеты')
        ]

    await bot.set_my_commands(main_menu_commands)