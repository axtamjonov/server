from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def get_start_admin():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(KeyboardButton("/start")).insert(KeyboardButton("/statistika")).add(KeyboardButton("/send_post"))
    btn.add(KeyboardButton("/get_user"))
    return btn

