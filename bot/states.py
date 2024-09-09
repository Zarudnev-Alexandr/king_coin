from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()


class WatchDailyStatSG(StatesGroup):
    start = State()


class EnterUserSG(StatesGroup):
    enter_id = State()
    enter_first_name = State()
    enter_last_name = State()
    enter_username = State()
    enter_finish = State()
    enter_after_finish = State()


