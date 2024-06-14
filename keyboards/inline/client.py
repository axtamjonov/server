from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_voice():
    ibtn = InlineKeyboardMarkup()
    ibtn.add(InlineKeyboardButton("👍", callback_data="like"))
    ibtn.add(InlineKeyboardButton("🤢", callback_data="dislike"))
    return ibtn