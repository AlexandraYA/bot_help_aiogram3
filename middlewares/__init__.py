from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from .throttling import ThrottlingMiddleware
from .support_middleware import SupportMiddleware


def register_middlewares(dp: Dispatcher):
   # storageThrottling = RedisStorage.from_url('redis://localhost:6379/0')
   # dp.message.middleware.register(ThrottlingMiddleware(storage=storageThrottling))
    dp.message.middleware.register(SupportMiddleware())
