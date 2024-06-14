import os

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
load_dotenv(find_dotenv())


CHANNELS = [{"name": "geekstest1", "id": "-1002158594501"}]
storage = MemoryStorage()
ADMIN = os.getenv("ADMIN")
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=storage)
