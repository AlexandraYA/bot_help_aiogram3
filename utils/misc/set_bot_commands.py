from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="support", description="Написать сообщение техподдержку"),
        BotCommand(command="support_call", description="Пообщаться с техподдержкой"),
        BotCommand(command="help", description="Помощь"),
    ])
