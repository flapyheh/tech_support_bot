from db.models import UsersORM, TicketsORM, MessagesORM
from db.database import async_engine, session_factory, Base
from enums.enums import Sender, Statuses

from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)

async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
async def insert_user(username : str, telegram_id : int) -> None:
    async with session_factory() as session:
        new_user = UsersORM(username = username, telegram_id = telegram_id)
        session.add(new_user)
        session.commit()
      
async def create_ticket(user_id : int) -> None:
    async with session_factory() as session:
        new_ticket = TicketsORM(user_id = user_id, status = Statuses.opened)
        session.add(new_ticket)
        await session.commit()
        
async def operator_took_ticket(operator_id : int, ticket_id : int):
    async with session_factory() as session:
        ticket = await session.get(TicketsORM, ticket_id)
        if ticket.operator_id is not None:
            logger.warning(f'Тикет уже используется оператором {ticket.operator_id}')
            return(False)
        else:
            ticket.operator_id = operator_id
            await session.commit()

async def insert_message(ticket_id : int, text : str, sender : Sender) -> None:
    async with session_factory() as session:
        ticket = session.get(TicketsORM, ticket_id)
        message = MessagesORM(ticket= ticket, text= text, sender= sender)
        session.add(message)
        session.commit()