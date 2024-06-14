import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline import get_voice
from keyboards.defoult import get_start, get_start_admin
from loader import bot, dp, ADMIN
from states import MyStates
from utils.database import users
from filters import isStr

like, dislike = 0, 0


@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    global like
    global dislike
    data = call.data
    if data == "like":
        like += 1
        await call.answer(f"like {like}")
    elif data == "dislike":
        dislike += 1
        await call.answer(f"dislike {dislike}")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == int(ADMIN):
        await message.answer("Assalomu aleykum hurmatli Hasanjon xush kelibsiz!", reply_markup=await get_start_admin())
    else:
        await message.answer("Xush kelibsiz", reply_markup=await get_start())
        user = users.get_user_by_id(message.from_user.id)
        if user:
            # fio = f"{message.from_user.first_name} {message.from_user.last_name}"
            users.create_user(message.from_user.id, message.from_user.username)
            await message.answer("Xush kelibsiz", reply_markup=await get_start())
            await message.answer("fio kiriting: ")
            await MyStates.about.set()


@dp.message_handler(state=MyStates.about)
async def about(message: types.Message):
    print("about - ", message.text)
    await message.answer("Qaysi kursda o'qimoqdasiz?", reply_markup=ReplyKeyboardRemove())
    await MyStates.courses.set()


@dp.message_handler(state=MyStates.courses)
async def about(message: types.Message, state: FSMContext):
    print("about - ", message.text)
    await message.answer("Rahmat")
    await state.finish()


# @dp.message_handler(state=MyStates.about)
# async def about(message: types.Message):
#     print("about - ", message.text)
#     await message.answer(text= "qaysi kursda o'qimoqdasiz'")
@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer("Tanglang: /photo yoki /sticker", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['sticker'])
async def sticker(message: types.Message):
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker="CAACAgIAAxkBAAEMJ5xmTCBtZR5_52SqYYr_xDF-KRTjZwACIwADWbv8JZG80mBAZfPHNQQ")


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact(message: types.Message):
    users.update_user(message.contact.phone_number, message.from_user.id)
    await message.answer("contact yozib olindi!")


@dp.message_handler(commands=['photo'])
async def photo(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://deneri.net/wp-content/uploads/2023/06/meyer-lemons-large-image.jpg",
                         caption="Sizga yoqdimi?", reply_markup=await get_voice())


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

@dp.message_handler(commands=["wheather"])
async def wheather(message: types.Message):
    res = requests.get("https://api.weatherapi.com/v1/current.json?key=637a0367057542d9936143247240705&q=Tashkent")
    if res.status_code == 200:
        response = res.json()
        name = response["location"]["name"]
        country = response["location"]["country"]
        tz = response["location"]["tz_id"]
        temp_c = response["current"]["temp_c"]

        text = (f"<em>Shahar</em> - <b>{name}</b>\n"
                f"<em>Davlat</em> - <b>{country}</b>\n"
                f"<em>Vaqt mintaqasi</em> - <b>{tz}</b>\n"
                f"<em>Harorat</em> - <b>{temp_c}°C</b>\n")
        await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["currency"])
async def currency(message: types.Message):
    res = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    if res.status_code == 200:
        response = res.json()
        for item in response:
            ccy = item["Ccy"]
            name = item["CcyNm_UZ"]
            rate = item["Rate"]
            if ccy == 'USD' or ccy == 'EUR' or ccy == 'RUB':
                text = (f"<b>{ccy}</b>\n"
                        f"1 {name} - {rate} so'm")
                await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["book"])
async def currency(message: types.Message):
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q=backend")
    if res.status_code == 200:
        response = res.json()
        for item in response:
            name = response["items"][0]["volumeInfo"]["title"]
            # sarlavha = response["items"][0]["volumeInfo"]["subtitle"]
            authors = response["items"][0]["volumeInfo"]["authors"][0]
            photo = response["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str = str(photo)

            name2 = response["items"][1]["volumeInfo"]["title"]
            # sarlavha2 = response["items"][1]["volumeInfo"]["subtitle"]
            authors2 = response["items"][1]["volumeInfo"]["authors"][0]
            photo2 = response["items"][1]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str2 = str(photo2)
            text = (f"<em>kitob nomi</em> - <b>{name}</b>\n"

                    f"<em>Avtor</em> - <b>{authors}</b>\n"
                    )
            text2 = (f"<em>2 - kitob nomi</em> - <b>{name2}</b>\n"
                     f"<em>Avtor</em> - <b>{authors2}</b>\n"
                     )
            name3 = response["items"][2]["volumeInfo"]["title"]
            # sarlavha3 = response["items"][2]["volumeInfo"]["subtitle"]
            authors3 = response["items"][2]["volumeInfo"]["authors"][0]
            photo3 = response["items"][2]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str3 = str(photo3)
            text3 = (f"<em>3 - kitob nomi</em> - <b>{name3}</b>\n"
                     f"<em>Avtor</em> - <b>{authors3}</b>\n"
                     )
            name4 = response["items"][3]["volumeInfo"]["title"]
            # sarlavha4 = response["items"][3]["volumeInfo"]["subtitle"]
            authors4 = response["items"][3]["volumeInfo"]["authors"][0]
            photo4 = response["items"][3]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str4 = str(photo4)
            text4 = (f"<em>4 - kitob nomi</em> - <b>{name4}</b>\n"

                     f"<em>Avtor</em> - <b>{authors4}</b>\n"
                     )
            name5 = response["items"][4]["volumeInfo"]["title"]
            # sarlavha5 = response["items"][4]["volumeInfo"]["subtitle"]
            authors5 = response["items"][4]["volumeInfo"]["authors"][0]
            photo5 = response["items"][4]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str5 = str(photo5)
            text5 = (f"<em>5 - kitob nomi</em> - <b>{name5}</b>\n"

                     f"<em>Avtor</em> - <b>{authors5}</b>\n"
                     )
            name6 = response["items"][5]["volumeInfo"]["title"]
            # sarlavha6 = response["items"][11]["volumeInfo"]["subtitle"]
            authors6 = response["items"][5]["volumeInfo"]["authors"][0]
            photo6 = response["items"][5]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str6 = str(photo6)
            text6 = (f"<em>6 - kitob nomi</em> - <b>{name6}</b>\n"

                     f"<em>Avtor</em> - <b>{authors6}</b>\n"
                     )
            name7 = response["items"][6]["volumeInfo"]["title"]
            # sarlavha7 = response["items"][6]["volumeInfo"]["subtitle"]
            authors7 = response["items"][6]["volumeInfo"]["authors"][0]
            photo7 = response["items"][6]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str7 = str(photo7)
            text7 = (f"<em>7 - kitob nomi</em> - <b>{name7}</b>\n"

                     f"<em>Avtor</em> - <b>{authors7}</b>\n"
                     )
            name8 = response["items"][7]["volumeInfo"]["title"]
            # sarlavha8 = response["items"][7]["volumeInfo"]["subtitle"]
            authors8 = response["items"][7]["volumeInfo"]["authors"][0]
            photo8 = response["items"][7]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str8 = str(photo8)
            text8 = (f"<em>8 - kitob nomi</em> - <b>{name8}</b>\n"

                     f"<em>Avtor</em> - <b>{authors8}</b>\n"
                     )
            name9 = response["items"][8]["volumeInfo"]["title"]
            # sarlavha9 = response["items"][8]["volumeInfo"]["subtitle"]
            authors9 = response["items"][8]["volumeInfo"]["authors"][0]
            photo9 = response["items"][8]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str9 = str(photo9)
            text9 = (f"<em>9 - kitob nomi</em> - <b>{name9}</b>\n"

                     f"<em>Avtor</em> - <b>{authors9}</b>\n"
                     )
            name10 = response["items"][9]["volumeInfo"]["title"]
            # sarlavha10 = response["items"][9]["volumeInfo"]["subtitle"]
            authors10 = response["items"][9]["volumeInfo"]["authors"][0]
            photo10 = response["items"][9]["volumeInfo"]["imageLinks"]["smallThumbnail"]
            photo_str10 = str(photo10)
            text10 = (f"<em>10 - kitob nomi</em> - <b>{name10}</b>\n"

                      f"<em>Avtor</em> - <b>{authors10}</b>\n"
                      )
        await message.answer(text, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str, caption="mana rasmi")
        await message.answer(text2, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str2, caption="mana rasmi")
        await message.answer(text3, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str3, caption="mana rasmi")
        await message.answer(text4, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str4, caption="mana rasmi")
        await message.answer(text5, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str5, caption="mana rasmi")
        await message.answer(text6, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str6, caption="mana rasmi")
        await message.answer(text7, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str7, caption="mana rasmi")
        await message.answer(text8, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str8, caption="mana rasmi")
        await message.answer(text9, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str9, caption="mana rasmi")
        await message.answer(text10, parse_mode="HTML")
        await bot.send_photo(chat_id=message.chat.id, photo=photo_str10, caption="mana rasmi")
@dp.message_handler(isStr())
async def echo(message: types.Message):
    await message.answer(message.text)