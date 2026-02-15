from aiogram import BaseMiddleware

from bot.db.query.orm import get_operator
from bot.handlers.operator import operator_router
from bot.handlers.user import user_router

class OperatorMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        operator = await get_operator(user.id)

        # Получаем router из data, если возможно
        router = data.get("router")

        if router is not None and router == operator_router:
            # Если в operator_router, но пользователь не оператор — отменяем обработку
            if operator is None:
                raise None  # прерываем вызов этого хендлера и роутера
        elif router is not None and router == user_router:
            # Если в user_router, но пользователь оператор — отменяем
            if operator is not None:
                raise None

        # Если всё ок, передаём дальше
        return await handler(event, data)