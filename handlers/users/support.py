from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from utils import SupportStates

from keyboards.inline.support import support_keyboard, StartSupCallback
from loader import bot


async def ask_support(message: Message):
    text = "Хотите написать сообщение техподдержке? Нажмите на кнопку ниже!"
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)


async def send_to_support(call: CallbackQuery, state: FSMContext, callback_data: StartSupCallback):
    await call.answer()
    user_id = int(callback_data.user_id)

    await call.message.answer("Пришлите ваше сообщение, которым вы хотите поделиться")
    await state.set_state(SupportStates.wait_for_support_message)
    await state.update_data(second_id=user_id)


async def get_support_message(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
 
    curr_state = str(
        await state.get_state()
    )
    print(curr_state)
    second_id = data.get("second_id")

    await bot.send_message(second_id,
                           f"Вам письмо! Вы можете ответить нажав на кнопку ниже")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer("Вы отправили это сообщение!")
    await state.clear()


def router(router: Router):
    router.message.register(get_support_message, SupportStates.wait_for_support_message)
    router.message.register(ask_support, Command(commands="support"))

    router.callback_query.register(send_to_support, StartSupCallback.filter(F.messages == "one"))
