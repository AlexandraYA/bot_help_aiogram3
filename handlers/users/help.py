from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


async def bot_help(message: Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))


def router(router: Router):
    router.message.register(bot_help,  Command(commands="help"))
