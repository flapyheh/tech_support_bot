import logging
from bot.bot_module import bot
from bot.lexicon.lexicon import RU
from bot.enums.enums import Sender
from bot.db.query.orm import insert_message, find_ticket_by_id, get_ticket_by_id

logger = logging.getLogger(__name__)

async def send_message_with_id(text : str, sender : Sender, ticket_id : int | None, id : str | None):
    if sender == Sender.operator:
        ticket = await get_ticket_by_id(ticket_id)
        if ticket is None:
            logger.warning(f'Нет тикета с таким айди {ticket_id}')
            return 'Такого айди тикета не существует!'
        await bot.send_message(chat_id= ticket.user_id, text= f'От ассистента поступил ответ: {text}', parse_mode=None)
        await insert_message(ticket_id=ticket_id, text=text, sender= Sender.user)
        logger.info(f'Сообщение от {sender.name} было отправлено в тикет {ticket_id}')
        return 'Сообщение отправлено пользователю!'
    else:
        ticket = await find_ticket_by_id(id)
        await insert_message(ticket_id=ticket.id, text=text, sender= Sender.user)
        logger.info(f'Сообщение от {sender.name} было отправлено на тикет {ticket.id}')
        if ticket.operator_id is not None:
            await bot.send_message(chat_id= ticket.operator_id, text= f'От пользователя на тикет {ticket_id} поступило сообщение: {text}')
            return 'Сообщение отправлено оператору!'
        return 'Сообщение отправлено, подождите пока ктото возьмет ваш тикет!'