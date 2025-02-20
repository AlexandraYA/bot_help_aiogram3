from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.storage.memory import StorageKey

from utils import SupportStates
from loader import dp
from keyboards.inline.support import support_keyboard, StartSupCallback, check_support_available, get_support_manager, \
    cancel_support, CancelSupCallback


async def ask_support_call(message: Message):
    text = "Хотите связаться с техподдержкой? Нажмите на кнопку ниже!"
    keyboard = await support_keyboard(messages="many")
    if not keyboard:
        await message.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await message.answer(text, reply_markup=keyboard)


async def send_to_support_call(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: StartSupCallback):
    await call.message.edit_text("Вы обратились в техподдержку. Ждем ответа от оператора!")

    user_id = int(callback_data.user_id)
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id

    if not support_id:
        await call.message.edit_text("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        await state.clear()
        return

    await state.set_state(SupportStates.wait_in_support)
    await state.update_data(second_id=support_id)

    user_state_str = str(await state.get_state())
    print(f'send_to_support_call user_state {user_state_str}')

    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(support_id,
                           f"С вами хочет связаться пользователь {call.from_user.full_name}",
                           reply_markup=keyboard
                           )


async def answer_support_call(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: StartSupCallback):
    second_id = int(callback_data.user_id)

    user_state: FSMContext = FSMContext(
            #bot=bot,  # объект бота
            storage=dp.storage,  # dp - экземпляр диспатчера
            key=StorageKey(
                chat_id=second_id,  # если юзер в ЛС, то chat_id=user_id
                user_id=second_id,
                bot_id=bot.id))

    user_state_name = await user_state.get_state()
    print(f'answer_support_call user_state {user_state_name}')

    if user_state_name != SupportStates.wait_in_support:
        await call.message.edit_text("К сожалению, пользователь уже передумал.")
        return

    await state.set_state(SupportStates.in_support)
    await user_state.set_state(SupportStates.in_support)

    await state.update_data(second_id=second_id)

    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(call.from_user.id)

    await call.message.edit_text("Вы на связи с пользователем!\n"
                                 "Чтобы завершить общение нажмите на кнопку.",
                                 reply_markup=keyboard
                                 )
    await bot.send_message(second_id,
                           "Техподдержка на связи! Можете писать сюда свое сообщение. \n"
                           "Чтобы завершить общение нажмите на кнопку.",
                           reply_markup=keyboard_second_user
                           )


async def not_supported(message: Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = cancel_support(second_id)
    await message.answer("Дождитесь ответа оператора или отмените сеанс", reply_markup=keyboard)


async def exit_support(call: CallbackQuery, bot: Bot, state: FSMContext, callback_data: CancelSupCallback):
    user_id = int(callback_data.user_id)

    second_state: FSMContext = FSMContext(
            #bot=bot,  # объект бота
            storage=dp.storage,  # dp - экземпляр диспатчера
            key=StorageKey(
                chat_id=user_id,  # если юзер в ЛС, то chat_id=user_id
                user_id=user_id,
                bot_id=bot.id))
    
    second_statee_str = str(await second_state.get_state())
    print(f'exit_support second_state {second_statee_str}')

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.clear()
            await bot.send_message(user_id, "Пользователь завершил сеанс техподдержки")

    await call.message.edit_text("Вы завершили сеанс")
    await state.clear()


def router(router: Router):
    router.message.register(ask_support_call, Command(commands="support_call"))
    router.message.register(not_supported, SupportStates.wait_in_support)
    router.message.register(not_supported, SupportStates.in_support)

    router.callback_query.register(send_to_support_call, StartSupCallback.filter(((F.messages == "many") & (F.as_user == "yes"))))
    router.callback_query.register(answer_support_call, StartSupCallback.filter(((F.messages == "many") & (F.as_user == "no"))))


    router.callback_query.register(exit_support, CancelSupCallback.filter())
