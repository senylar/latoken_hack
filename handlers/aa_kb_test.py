from curses.ascii import isdigit

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.state import StateFilter
from loader import bot, assistant
from promts import promt4test
from config import openai_api_key, knowledge_base_promt, assistant_id
from chat_gpt_api import OpenAIChatGPT
from models import QueryResponse
from db.db import insert_query_response, get_query_response

router = Router()

class Test(StatesGroup):
    question = State()
    results = State()

@router.message(Command(commands=['test']))
async def test(message: types.Message, state: FSMContext):
    await state.set_state(Test.question)
    await bot.send_chat_action(message.chat.id, action='typing')


    response = await assistant.get_response(assistant_id, message.chat.id, promt4test)
    await state.update_data(scores=[], count=0)
    await message.answer(response)

@router.message(StateFilter(Test.question))
async def answer_for_q(message: types.Message, state: FSMContext):
    response = await assistant.get_response(assistant_id, message.chat.id, message.text)
    if isdigit(response[0]):
        num = int(response[0])
        if isdigit(response[1]):
            num = 10
        data = await state.get_data()
        data['scores'].append(num)
        data['count'] += 1
        await state.update_data(scores=data['scores'], count=data['count'])

        if data['count'] == 2:
            await state.set_state(Test.results)
    await message.answer(response)

@router.message(StateFilter(Test.results))
async def results(message: types.Message, state: FSMContext):
    response = await assistant.get_response(assistant_id, message.chat.id, message.text+'это ответ на последний вопрос, не задавай следующий.')
    await message.answer(response)
    data = await state.get_data()
    data['scores'].append(int(response[0]))
    await message.answer(f'Ваш средний бал {sum(data["scores"]) / len(data["scores"])}')
    await state.clear()