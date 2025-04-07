from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


async def bot_help(message: Message):
    text = ("Список команд: ",
            "/start - Запустить бота",
            "/support - Написать в техподдержку",
            "/help - Список команд")
    
    await message.answer("\n".join(text))


def router(router: Router):
    router.message.register(bot_help,  Command(commands="help"))
