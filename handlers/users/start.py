from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

async def bot_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Привет, {message.from_user.full_name}!")

def router(router: Router):
    router.message.register(bot_start, CommandStart())
