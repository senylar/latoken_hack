import asyncio

import aiofiles

from chat_gpt_api import OpenAIChatGPT


class OpenAIChatManager:
    def __init__(self, api_key: str, knowledge_base_path: str):
        """
        Initialize OpenAIChatManager and pre-load the knowledge base.

        :param api_key: OpenAI API key.
        :param knowledge_base_path: Path to the text file containing the knowledge base.
        """
        self.api_key = api_key
        self.knowledge_base_path = knowledge_base_path
        self.chat_instance = None

        # Load knowledge base at initialization
        loop = asyncio.get_event_loop()
        self.knowledge_base = loop.run_until_complete(self._load_knowledge_base())



    async def _load_knowledge_base(self):
        """Load knowledge base from file."""
        async with aiofiles.open(self.knowledge_base_path, 'r', encoding='utf-8') as file:
            return await file.read()

    async def __aenter__(self):
        """Create an OpenAIChatGPT instance with pre-loaded knowledge base."""
        self.chat_instance = OpenAIChatGPT(self.api_key, self.knowledge_base)
        return self.chat_instance

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Cleanup the instance."""
        self.chat_instance = None  # Allow garbage collection