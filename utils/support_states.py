from aiogram.fsm.state import State, StatesGroup


class SupportStates(StatesGroup):
    wait_for_support_message = State()
    wait_in_support = State()
    in_support = State()
