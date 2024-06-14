from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from loader import CHANNELS, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ChannelMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        print(message.text)
        user = message.from_user
        if user.username:
            ibtn = InlineKeyboardMarkup()
            for channel in CHANNELS:
                user_channel = await bot.get_chat_member(user_id=int(user.id), chat_id=channel.get("id"))
                if user_channel.status == "left":
                    ibtn.add(
                        InlineKeyboardButton(text=channel.get("name"), url=f"https://t.me/{channel.get('name')}")
                    )
                    await message.answer("iltimos kanalga a'zo bo'ling!!!", reply_markup=ibtn)
