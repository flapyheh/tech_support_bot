import logging
import shlex
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.enums.enums import Sender
from bot.lexicon.lexicon import RU
from bot.services.sender import send_message_with_id

logger = logging.getLogger(__name__)
operator_router = Router()

@operator_router.message(Command('ticket'))
async def process_ticket_answer(message: Message):
    args = shlex.split(message.text)
    
    if len(args) < 3:
        await message.reply("Использование: /ticket <ticket_id> <сообщение>\nПример: /ticket 1234 Ваша проблема", parse_mode=None)
        return
    
    ticket_id = args[1]
    msg_content = ' '.join(args[2:])
    
    try:
        result = await send_message_with_id(text= msg_content, sender= Sender.operator, ticket_id= int(ticket_id), id= None)
        await message.answer(result)
    except Exception as e:
        logger.warning(f'Ошибка при обработке тикета {ticket_id}: {e}')
        await message.reply("Произошла ошибка при обработке вашего сообщения.")
    
@operator_router.message()
async def process_ticket_answer(message: Message):
    await message.answer(text= RU['operator_other'])