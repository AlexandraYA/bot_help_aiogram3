import asyncio
import logging
import sys
from typing import Any
from aiogram import Router

from loader import bot, dp
from utils.misc.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify
from middlewares import register_middlewares
from handlers import register_routers

async def on_startup():
    # Уведомляет про запуск
    await set_default_commands(bot)
    await on_startup_notify(bot)

async def on_shutdown() -> Any:
    print("Бот лёг")

async def main():
    # #### include Private chat router ########
    # for pr_router in private_routers:
    #    dp.include_router(pr_router)

    register_middlewares(dp)

    main_router = Router()
    register_routers(main_router)
    dp.include_router(main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
