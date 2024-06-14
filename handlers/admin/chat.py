from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, ADMIN, bot
from utils.database import users
from states import MyAdminStates
from filters import isAdmin


@dp.message_handler(isAdmin(), commands=["users"])
async def get_user(message: types.Message):
    global texti
    if message.from_user.id == int(ADMIN):
        user = users.get_users()
        for item in user:
            texti = (f"<i>FIO</i> - <b>{item[1]}</b>\n"
                     f"<i>USERNAME</i> - <b>{item[2]}</b>\n"
                     f"<i>CHAT ID</i> - <b>{item[3]}</b>\n"
                     f"<i>PHONE NUMBER</i> - <b>{item[1]}</b>\n")
        await message.answer(text=texti, parse_mode="HTML")


@dp.message_handler(commands=["about_me"])
async def about_me(message: types.Message):
    global text
    if message.from_user.id == message.chat.id:
        info = users.about_me(message.from_user.id)
        for item in info:
            text = (f"<i>FIO</i> - <b>{item[1]}</b>\n"
                    f"<i>USERNAME</i> - <b>{item[2]}</b>\n"
                    f"<i>CHAT ID</i> - <b>{item[3]}</b>\n"
                    f"<i>PHONE NUMBER</i> - <b>{item[1]}</b>\n")
    await message.answer(text=text, parse_mode="HTML")



@dp.message_handler(commands=["send_post"])
async def send_post(message: types.Message):
    if message.from_user.id==int(ADMIN):
        await message.answer("messageni kiritiing: ")
        await MyAdminStates.message.set()

@dp.message_handler(state=MyAdminStates.message)
async def send_message(message: types.Message, state: FSMContext):
    if message.from_user.id==int(ADMIN):
        user = users.get_users()
        if len(user) > 0:
            for item in user:
                print(item)
                await bot.send_message(item[3], message.text)
                await state.finish()