from abc import ABC, abstractmethod

class ChatAPI(ABC):

    @abstractmethod
    def __init__(self, api_key: str):
        """
        Инициализирует класс API.

        :param api_key: Ключ API
        """
        pass

    @abstractmethod
    async def get_response(self, user_query: str) -> str:
        """
        Получает ответ от API на запрос пользователя.

        :param user_query: Запрос пользователя
        :return: Ответ от API
        """
        pass

