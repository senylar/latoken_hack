from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from chat_gpt_api.assistant import OpenAIAssistantManager
from config import telegram_bot_token, openai_api_key


bot = Bot(token=telegram_bot_token, default=DefaultBotProperties(parse_mode='MARKDOWN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


assistant = OpenAIAssistantManager(api_key=openai_api_key)
print(openai_api_key)


