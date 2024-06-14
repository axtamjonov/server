from aiogram.dispatcher.filters.state import StatesGroup, State

class MyStates(StatesGroup):
    about = State()
    courses = State()
class MyAdminStates(StatesGroup):
    message = State()