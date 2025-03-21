from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот-помощник Latoken. Чем могу помочь?",
                         reply_markup=types.ReplyKeyboardRemove())



@router.message(Command(commands=['t']))
async def g(message: types.Message):

    t = '''
    1. Несоответствие сниппета задачам проекта, что приводит к нарушению правила о том, что из названия проекта должно быть понятно, какие задачи в нем находятся[14:0†-210.txt](https://coda.io/@latoken/latoken-talent/-210).
2. Нарушение правил Scrum, связанных с определением и структурированием задач, которое приводит к увольнению сотрудника【14:1†-210.txt】.
3. Конфликт интересов и задействование в параллельных проектах (freelance project), что ведет к конфликту интересов и нарушению этического кодекса компании【14:2†long-hour-rule-142.txt]'''
    await message.answer(t)