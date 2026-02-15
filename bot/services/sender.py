import logging
from bot.bot_module import bot
from bot.lexicon.lexicon import RU
from bot.enums.enums import Sender, Statuses
from bot.db.query.orm import change_ticket_status, change_user_state, get_user_by_ticket, insert_message, find_ticket_by_id, get_ticket_by_id

logger = logging.getLogger(__name__)

async def send_message_with_id(text : str, sender : Sender, ticket_id : int | None, id : str | None):
    if sender == Sender.operator:
        ticket = await get_ticket_by_id(ticket_id)
        if ticket is None:
            logger.warning(f'Нет тикета с таким айди {ticket_id}')
            return 'Такого айди тикета не существует!'
        if ticket.operator_id != id:
            logger.warning(f'Тикет уже взял оператор {ticket.operator_id}')
            return 'Тикет взял другой оператор!'
        if ticket.status == Statuses.closed:
            logger.warning(f'Тикет {ticket.id} уже закрыт')
            return 'Тикет уже закрыт!'
        await bot.send_message(chat_id= ticket.user_id, text= f'От ассистента поступил ответ: {text}', parse_mode=None)
        await insert_message(ticket_id=ticket_id, text=text, sender= Sender.operator)
        logger.info(f'Сообщение от {sender.name} было отправлено в тикет {ticket_id}')
        return 'Сообщение отправлено пользователю!'
    else:
        ticket = await find_ticket_by_id(id)
        await insert_message(ticket_id=ticket.id, text=text, sender= Sender.user)
        logger.info(f'Сообщение от {sender.name} было отправлено на тикет {ticket.id}')
        if ticket.operator_id is not None:
            await bot.send_message(chat_id= ticket.operator_id, text= f'От пользователя на тикет {ticket.id} поступило сообщение: {text}')
            return 'Сообщение отправлено оператору!'
        return 'Сообщение отправлено, подождите пока ктото возьмет ваш тикет!'
    
async def close_ticket_sender(ticket_id : int) -> str:
    await change_ticket_status(ticket_id=ticket_id, state= Statuses.closed)
    user = await get_user_by_ticket(ticket_id=ticket_id)
    await change_user_state(telegram_id=user.telegram_id, state= False)
    await bot.send_message(chat_id=user.telegram_id, text='Ваш тикет был закрыт оператором!')
    return 'Тикет закрыт'