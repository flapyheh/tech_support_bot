from typing import Optional
from bot.db.models import UsersORM, TicketsORM, MessagesORM, OperatorsORM
from bot.db.database import async_engine, session_factory, Base
from bot.enums.enums import Sender, Statuses

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)

async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
async def insert_user(username : str, telegram_id : int) -> None:
    async with session_factory() as session:
        new_user = UsersORM(username = username, telegram_id = telegram_id, isOnTicket = False)
        session.add(new_user)
        await session.commit()
        logger.info(f'Пользователь {telegram_id} зашел в бота')
        
async def change_user_state(telegram_id : int, state : bool) -> None:
    async with session_factory() as session:
        user = await session.execute(
            select(UsersORM).where(UsersORM.telegram_id == telegram_id)
        )
        user = user.scalars().first()
        user.isOnTicket = state
        await session.commit()
        logger.info(f'Пользователь {telegram_id} поменял состояние на {state}')
        
async def insert_all_operators(operator_ids : list[int]) -> None:
    async with session_factory() as session:
        operators = []
        for id in operator_ids:
            new_operator = OperatorsORM(telegram_id=id)
            operators.append(new_operator)
        session.add_all(operators)
        await session.commit()
        logger.info('Операторы добавлены в БД')
      
async def create_ticket(user_id : int) -> None:
    async with session_factory() as session:
        new_ticket = TicketsORM(user_id = user_id, status = Statuses.opened)
        session.add(new_ticket)
        await session.commit()
        logger.info('Тикет создан')
        
async def operator_took_ticket(operator_id : int, ticket_id : int):
    async with session_factory() as session:
        ticket = await session.get(TicketsORM, ticket_id)
        if ticket is not None:
            if ticket.operator_id is not None:
                logger.warning(f'Тикет уже используется оператором {ticket.operator_id}')
                return('Тикет уже под рассмотром')
            else:
                ticket.operator_id = operator_id
                await session.commit()
                return(f'Вы взяли тикет с id {ticket_id}')
        else:
            logger.warning('Оператор ввел неправильный id тикета')
            return('Такого тикета не существует!')
        
async def find_ticket_by_id(user_id : int) -> Optional[TicketsORM]:
    async with session_factory() as session:
        query = select(TicketsORM).where(and_(TicketsORM.user_id == user_id, TicketsORM.status == Statuses.opened))
        result = await session.execute(query)
        ticket = result.scalars().first()
        return ticket
    
async def get_ticket_by_id(ticket_id : int) -> Optional[TicketsORM]:
    async with session_factory() as session:
        query = select(TicketsORM).where(and_(TicketsORM.id == ticket_id, TicketsORM.status == Statuses.opened))
        result = await session.execute(query)
        ticket = result.scalars().first()
        return ticket

async def insert_message(ticket_id : int, text : str, sender : Sender) -> None:
    async with session_factory() as session:
        ticket = await session.get(TicketsORM, ticket_id)
        message = MessagesORM(ticket= ticket, text= text, sender= sender)
        session.add(message)
        logger.info(f'message {message.id} added to ticket {ticket.id}')
        await session.commit()
        
async def get_operator(telegram_id : int) -> OperatorsORM | None:
    async with session_factory() as session:
        result = await session.execute(select(OperatorsORM).where(OperatorsORM.telegram_id == telegram_id))
        operator = result.scalars().first()
        logger.info('Получили оператора')
        return(operator)

async def get_user(telegram_id : int) -> UsersORM | None:
    async with session_factory() as session:
        result = await session.execute(select(UsersORM).where(UsersORM.telegram_id == telegram_id))
        user = result.scalars().first()
        logger.info('Получили пользователя')
        return(user)

async def get_all_opened_tickets() -> list[TicketsORM] | None:
    async with session_factory() as session:
        result = await session.execute(select(TicketsORM).where(TicketsORM.status == Statuses.opened))
        tickets = result.scalars().all()
        return(tickets)
    
async def change_ticket_status(ticket_id : int, state : bool) -> str:
    async with session_factory() as session:
        ticket = await session.get(TicketsORM, ticket_id)
        if ticket is None:
            return 'Такого тикета не существует!'
        ticket.status = state
        logger.info(f'Тикет {ticket_id} поменял состояние на {state}')
        await session.commit()
        
async def get_user_by_ticket(ticket_id : int) -> UsersORM | None:
    async with session_factory() as session:
        ticket = await session.get(TicketsORM, ticket_id)
        if ticket is None:
            return None
        result = await session.execute(select(UsersORM).where(UsersORM.telegram_id == ticket.user_id))
        user = result.scalars().first()
        return user

async def get_all_msg_from_ticket(ticket_id : int) -> list[MessagesORM] | None:
    async with session_factory() as session:
        result = await session.execute(select(TicketsORM).where(TicketsORM.id == ticket_id).options(joinedload(TicketsORM.messages)))
        ticket = result.scalars().first()
        if ticket is None:
            return None
        return ticket.messages