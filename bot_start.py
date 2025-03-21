import asyncio
from aiogram import Dispatcher
from loader import bot, dp
from handlers.start import router as start_router
from handlers.answer_for_q import router as answer_for_q_router
from handlers.aa_kb_test import router as kb_test_router
from db.db import create_table
from admins.recreate_assistent import router as recreate_assistent_router

async def main():
    dp.include_router(recreate_assistent_router)
    dp.include_router(kb_test_router)
    dp.include_router(start_router)
    dp.include_router(answer_for_q_router)


    await dp.start_polling(bot)
    await create_table()

if __name__ == "__main__":
    asyncio.run(main())