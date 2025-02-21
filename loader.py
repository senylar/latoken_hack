from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import telegram_bot_token

bot = Bot(token=telegram_bot_token, default=DefaultBotProperties(parse_mode='MARKDOWN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)