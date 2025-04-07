import random

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import StorageKey

from data.config import support_ids
from loader import dp, bot

class StartSupCallback(CallbackData, prefix="start"):
    call: str
    messages: str
    user_id: int
    as_user: str

class CancelSupCallback(CallbackData, prefix="cancel"):
    call: str
    user_id: int

async def check_support_available(support_id):
    # state = bot.current_state(chat=support_id, user=support_id)

    state: FSMContext = FSMContext(
            #bot=bot,  # объект бота
            storage=dp.storage,  # dp - экземпляр диспатчера
            key=StorageKey(
                chat_id=support_id,  # если юзер в ЛС, то chat_id=user_id
                user_id=support_id,
                bot_id=bot.id))

    state_str = str(
        await state.get_state()
    )

    if state_str == "in_support":
        return
    else:
        return support_id


async def get_support_manager():
    random.shuffle(support_ids)
    for support_id in support_ids:
        # Проверим если оператор в данное время не занят
        support_id = await check_support_available(support_id)

        # Если такого нашли, что выводим
    if support_id:
        return support_id
    else:
        return


async def support_keyboard(messages, user_id=None):
    
    if user_id:
        # Есле указан второй айдишник - значит эта кнопка для оператора

        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю"

    else:
        # Есле не указан второй айдишник - значит эта кнопка для пользователя
        # и нужно подобрать для него оператора

        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            # Если не нашли свободного оператора - выходим и говорим, что его нет
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(support_ids)

        if messages == "one":
            text = "Написать 1 сообщение в техподдержку"
        else:
            text = "Написать оператору"



    builder = InlineKeyboardBuilder()
    builder.button(
            text=text,
            callback_data=StartSupCallback(
                call='ask_support',
                messages=messages,
                user_id=contact_id,
                as_user=as_user).pack()
    )

    if messages == "many":
        # Добавляем кнопку завершения сеанса, если передумали звонить в поддержку
        builder.button(
                text="Завершить сеанс",
                callback_data=CancelSupCallback(call='cancel_support', user_id=contact_id).pack()
        )
    return builder.as_markup()


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=CancelSupCallback(call='cancel_support', user_id=user_id).pack()
                )
            ]
        ]
    )
