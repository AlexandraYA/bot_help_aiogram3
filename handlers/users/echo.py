from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
async def bot_echo(message: Message):
    await message.answer(f"Эхо без состояния."
                         f"Сообщение:\n"
                         f"{message.text}")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
async def bot_echo_all(message: Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")

def router(router: Router):
    router.message.register(bot_echo, StateFilter(None))
   # router.message.register(bot_echo_all)
