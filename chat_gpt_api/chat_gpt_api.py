# -*- coding: utf-8 -*-

import os
import asyncio
from .chat_api_scheme import ChatAPI

import aiofiles
from openai import AsyncOpenAI

class OpenAIChatGPT(ChatAPI):
    def __init__(self, api_key: str, knowledge_base_promt: str):
        """
        Initialize the OpenAIChatGPT class.

        :param api_key: Your OpenAI API key.
        :param knowledge_base_path: Path to the text file representing the knowledge base.
        """
        self.api_key = api_key
        print(self.api_key)
        self.knowledge_base_promt = knowledge_base_promt
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def load_knowledge_base(self) -> str:
        """
        Load the knowledge base from the text file.

        :return: The content of the knowledge base.
        """
        async with aiofiles.open(self.knowledge_base_path, 'r', encoding='utf-8') as file:
            knowledge_base = await file.read()
        return knowledge_base

    async def generate_messages(self, user_query: str) -> list:
        """
        Generate a list of messages by combining the user query and knowledge base.

        :param user_query: The user's query.
        :return: The list of messages.
        """
        context_message = {
            "role": "system",
            "content": self.knowledge_base_promt
        }
        user_message = {
            "role": "user",
            "content": user_query
        }
        return [context_message, user_message]

    async def get_response(self, user_query: str) -> str:
        """
        Get a response from the OpenAI API based on the user query and knowledge base.

        :param user_query: The user's query.
        :return: The response from the OpenAI API.
        """
        messages = await self.generate_messages(user_query)
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content



# Example usage:
async def main():
    from config import openai_api_key
    api_key = openai_api_key
    knowledge_base_path = "/kb/knowledge_base.txt"
    chatgpt = OpenAIChatGPT(api_key, knowledge_base_path)
    user_query = "Какими качествами я должен обладать?"
    response = await chatgpt.get_response(user_query)
    print(response)

