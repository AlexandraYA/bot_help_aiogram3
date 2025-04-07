from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.fsm.storage.memory import StorageKey

from loader import dp, bot
from utils import SupportStates


# Создадим миддлварь, в котором полностью будет  проходить обработка сообщений
# для пользователя и операторов, которые находятся на связи.
# Отсюда сообщения в хендлеры даже направляться не будут
class SupportMiddleware(BaseMiddleware):
    
  async def __call__(self,
                     handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                     event: Message,
                     data: Dict[str, Any]
                     ) -> Any:
        # Для начала достанем состояние текущего пользователя,
        # так как state: FSMContext нам сюда не прилетит
        state: FSMContext = FSMContext(
            #bot=bot,  # объект бота
            storage=dp.storage,  # dp - экземпляр диспатчера
            key=StorageKey(
                chat_id=event.from_user.id,  # если юзер в ЛС, то chat_id=user_id
                user_id=event.from_user.id,
                bot_id=bot.id))

        # Получим строчное значение стейта и сравним его
        state_name = await state.get_state()

        if state_name == SupportStates.in_support:
            # Заберем айди второго пользователя и отправим ему сообщение
            data = await state.get_data()
            second_id = data.get("second_id")
            await event.copy_to(second_id)
        else:
            return await handler(event, data)
