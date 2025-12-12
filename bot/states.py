from aiogram.fsm.state import StatesGroup, State

class TaskCreation(StatesGroup):
choosing_assignee = State()
entering_title = State()
setting_datetime = State()

class TaskReschedule(StatesGroup):
waiting_new_datetime = State()