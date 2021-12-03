from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='token_your_bot_from_botfather', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())