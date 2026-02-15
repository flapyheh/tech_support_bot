import logging
import shlex
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.enums.enums import Sender
from bot.lexicon.lexicon import RU
from bot.services.sender import send_message_with_id, close_ticket_sender
from bot.db.query.orm import get_all_msg_from_ticket, operator_took_ticket, get_all_opened_tickets, change_ticket_status
from bot.keyboards.menu import set_main_menu

logger = logging.getLogger(__name__)
operator_router = Router()

@operator_router.message(CommandStart())
async def process_ticket_answer(message: Message):
    await message.reply(RU['start_operator'])
    await set_main_menu()

@operator_router.message(Command('ticket'))
async def process_ticket_answer(message: Message):
    logger.info(f'Зашли в /ticket хэндлер')
    args = shlex.split(message.text)
    
    if len(args) < 3:
        await message.reply("Использование: /ticket <ticket_id> <сообщение>\nПример: /ticket 1234 Ваш ответ", parse_mode=None)
        return
    
    ticket_id = args[1]
    msg_content = ' '.join(args[2:])
    
    try:
        result = await send_message_with_id(text= msg_content, sender= Sender.operator, ticket_id= int(ticket_id), id= message.from_user.id)
        await message.answer(result)
    except Exception as e:
        logger.warning(f'Ошибка при обработке тикета {ticket_id}: {e}')
        await message.reply("Произошла ошибка при обработке вашего сообщения.")
        
@operator_router.message(Command('took'))
async def process_ticket_answer(message: Message):
    logger.info('зашли в хэндлер took')
    args = shlex.split(message.text)
    
    if len(args) != 2:
        await message.reply("Использование: /took <ticket_id>\nПример: /took 1234", parse_mode=None)
        return
    
    ticket_id = args[1]
    try:
        result = await operator_took_ticket(operator_id= message.from_user.id, ticket_id= int(ticket_id))
        await message.reply(result)
    except Exception as e:
        logger.warning(f'Ошибка при обработке тикета {ticket_id}: {e}')
        await message.reply("Произошла ошибка при обработке вашего сообщения.")

@operator_router.message(Command('tickets'))
async def process_ticket_answer(message: Message):
    logger.info('Зашли в хэндлер tickets')
    tickets = await get_all_opened_tickets()
    ticket_ids = []
    for ticket in tickets:
        ticket_ids.append(ticket.id)
    text = '\n'.join(f"{i+1}) {ticket_id}" for i, ticket_id in enumerate(ticket_ids))
    await message.answer(f'Все тикеты которые свободны на данный момент:\n{text}')

@operator_router.message(Command('close'))
async def process_ticket_answer(message: Message):
    logger.info('Зашли в хэндлер close')
    args = shlex.split(message.text)
    
    if len(args) != 2:
        await message.reply("Использование: /close <ticket_id>\nПример: /close 1234", parse_mode=None)
        return
    
    ticket_id = args[1]
    try:
        await close_ticket_sender(ticket_id=int(ticket_id))
    except Exception as e:
        logger.warning(f'Ошибка при обработке тикета {ticket_id}: {e}')
        await message.reply("Произошла ошибка при обработке вашего сообщения.")
        
@operator_router.message(Command('show'))
async def process_ticket_answer(message: Message):
    logger.info('Зашли в хэндлер show')
    args = shlex.split(message.text)
    
    if len(args) != 2:
        await message.reply("Использование: /show <ticket_id>\nПример: /show 1234", parse_mode=None)
        return
    
    ticket_id = args[1]
    try:
        messages = await get_all_msg_from_ticket(ticket_id=int(ticket_id))
        await message.answer(f'Отправитель {msg.sender.name}. Текст: {msg.text}\n' for msg in messages)
    except Exception as e:
        logger.warning(f'Ошибка при обработке тикета {ticket_id}: {e}')
        await message.reply("Произошла ошибка при обработке вашего сообщения.")
        
@operator_router.message()
async def process_ticket_answer(message: Message):
    logger.info(f'Зашли в other хэндлер')
    await message.answer(text= RU['operator_other'])