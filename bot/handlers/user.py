import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.filters.filters import TicketFilter
from bot.lexicon.lexicon import RU
from bot.keyboards.keyboards import keyboard_user
from bot.db.query.orm import insert_user, create_ticket, get_user, change_user_state
from bot.enums.enums import Sender
from bot.services.sender import send_message_with_id

logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def process_start_user_command(message : Message):
    logger.info('Зашли в user хэндлер /start')
    user = await get_user(message.from_user.id)
    if user is None:
        await message.answer(
            text= RU['start'],
            reply_markup=keyboard_user
        )
        await insert_user(message.from_user.username, message.from_user.id)
    logger.info(f'Пользователь {message.from_user.id} запустил бота')
    
@user_router.callback_query(F.data == RU['user_help_call'])
async def process_open_ticket(call : CallbackQuery):
    logger.info('Пользователь нажал на кнопку обращения в поддежку')
    await call.message.edit_text(
        text= RU['helper_text'],
        reply_markup=None
    )
    await change_user_state(call.from_user.id, True)
    await create_ticket(user_id= call.from_user.id)
    
@user_router.message(TicketFilter())
async def process_ticket_appeal(message : Message):
    result = await send_message_with_id(text= message.text, sender= Sender.user, id= message.from_user.id)
    await message.answer(result)

@user_router.message()
async def process_ticket_appeal(message : Message):
    await message.answer(
        text= RU['no_ticket'],
        reply_markup=keyboard_user
    )