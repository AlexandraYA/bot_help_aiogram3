from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="support", description="Написать в техподдержку"),
        BotCommand(command="help", description="Помощь"),
    ])
