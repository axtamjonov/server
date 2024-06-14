from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def get_start():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(KeyboardButton("/start")).insert(KeyboardButton("/help"))
    btn.add(KeyboardButton("/sticker")).add(KeyboardButton("/photo"))
    btn.add(KeyboardButton("/contact ☎️", request_contact=True))
    return btn