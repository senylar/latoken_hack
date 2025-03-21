from filters.filters import IsAdmin
from aiogram import Router, types
from aiogram.filters import CommandStart
from loader import bot, assistant

from config import openai_api_key, knowledge_base_promt, assistant_id
from chat_gpt_api import OpenAIChatGPT
from models import QueryResponse
from db.db import insert_query_response, get_query_response
from aiogram.filters import Command
from utils import return_cyclic_elements
from loader import assistant
from config import assistant_id

router = Router()

@router.message(Command(commands=['recreate']))
async def recreate(message: types.Message):
    global assistant_id
    print('start')
    assistant_id = await assistant.create_assistant(files_dir='kb')

    print(assistant_id)