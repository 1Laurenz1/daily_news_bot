from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class NotificationTimeState(StatesGroup):
    notification_time = State()