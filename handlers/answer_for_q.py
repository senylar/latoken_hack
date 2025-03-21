from aiogram import Router, types
from aiogram.filters import CommandStart
from loader import bot, assistant

from config import openai_api_key, knowledge_base_promt, assistant_id
from chat_gpt_api import OpenAIChatGPT
from models import QueryResponse
from db.db import insert_query_response, get_query_response
from aiogram.filters import Command
from utils import return_cyclic_elements

router = Router()



@router.message(Command(commands=['g']))
async def g(message: types.Message):

    resp = await get_query_response(int(message.text.split(' ')[1]))
    print(resp)
    await message.answer(resp)




@router.message(lambda message: not message.text.startswith('/'))
async def answer_for_q(message: types.Message):
    # Создание объекта для работы с OpenAI Chat GPT

    await bot.send_chat_action(message.chat.id, action='typing')
    chat_gpt = OpenAIChatGPT(api_key=openai_api_key, knowledge_base_promt=knowledge_base_promt)
    answer = await chat_gpt.get_response(message.text)
    g = return_cyclic_elements()
    if 'НЕ ХВАТАЕТ' in answer:
        m = await message.answer('Ищу в базе данных: ')

        answer = await assistant.get_response(assistant_id,message.chat.id, message.text, message=m, g=g)

    await message.answer(answer)

    #Запись запроса и ответа в базу данных
    query_response = QueryResponse(query=message.text, answer=answer)
    print(query_response)
    await insert_query_response(query_response)


