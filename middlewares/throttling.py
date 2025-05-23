from typing import Any, Awaitable, Callable, Dict

import asyncio

from aiogram.types import Message, TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage


class ThrottlingMiddleware(BaseMiddleware):
  def __init__(self, storage: RedisStorage):
    self.storage = storage


  async def __call__(self,
                     handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                     event: Message,
                     data: Dict[str, Any]
                     ) -> Any:
    user = f'user{event.from_user.id}'

    check_user = await self.storage.redis.get(name=user)

    if check_user:
      if int(check_user.decode()) == 1:
        await self.storage.redis.set(name=user, value=0, ex=10)
        return await event.answer('Мы обнаружили подозрительную активность. Ждите 10 секунд.')
      return
    await self.storage.redis.set(name=user, value=1, ex=10)

    return await handler(event, data)


