import asyncio
from aiogram import Dispatcher
from loader import bot, dp
from handlers.start import router as start_router
from handlers.answer_for_q import router as answer_for_q_router

async def main():
    dp.include_router(start_router)
    dp.include_router(answer_for_q_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())