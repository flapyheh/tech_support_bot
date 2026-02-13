from typing import Any, Awaitable, Callable
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from bot.db.query.orm import get_operator

logger = logging.getLogger(__name__)

class OperatorMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        logger.info(f'Зашли в миддлварь')
        user: User = data.get("event_from_user")

        operator = await get_operator(user.id)
        if operator is not None:
            return await handler(event, data)
        else:
            return