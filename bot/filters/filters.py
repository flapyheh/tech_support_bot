from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from bot.db.query.orm import get_operator, get_user

class OperatorFilter(BaseFilter):
    async def __call__(self, message : Message | CallbackQuery):
        operator = await get_operator(message.from_user.id)
        if operator is None:
            return False
        else:
            return True
        
class UserFilter(BaseFilter):
    async def __call__(self, message : Message | CallbackQuery):
        user = await get_user(message.from_user.id)
        if user is None:
            return False
        else:
            return True
        
class TicketFilter(BaseFilter):
    async def __call__(self, message : Message):
        user = await get_user(message.from_user.id)
        if user is None:
            return False
        return user.isOnTicket