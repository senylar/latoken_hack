from aiogram import Router, types
from aiogram.filters import CommandStart
from loader import bot

from config import openai_api_key, knowledge_base_promt
from chat_gpt_api import OpenAIChatGPT

router = Router()

@router.message()
async def answer_for_q(message: types.Message):
    # Создание объекта для работы с OpenAI Chat GPT

    await bot.send_chat_action(message.chat.id, action='typing')

    chat_gpt = OpenAIChatGPT(api_key=openai_api_key, knowledge_base_promt=knowledge_base_promt)
    answer = await chat_gpt.get_response(message.text)

    await message.answer(answer)