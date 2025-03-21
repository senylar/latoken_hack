from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
from config import admins


router = Router()


class IsAdmin(Filter):
    def __init__(self, admins: str) -> None:
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        return message.chat.id in self.admins


