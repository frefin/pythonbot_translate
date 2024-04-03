from aiogram.fsm.state import State, StatesGroup

class TranslateFSM(StatesGroup):
    lang_1 = State()
    text = State()