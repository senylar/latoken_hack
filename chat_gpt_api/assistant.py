import openai
import asyncio
import os

class OpenAIAssistantManager:
    def __init__(self, api_key: str):
        self.user_threads = {}
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def upload_files(self, files_dir: str) -> list:
        file_ids = []
        for filename in os.listdir(files_dir):
            file_path = os.path.join(files_dir, filename)
            if os.path.isfile(file_path):
                file = await self.client.files.create(
                    file=open(file_path, "rb"),
                    purpose="assistants"                )
                file_ids.append(file.id)
        return file_ids

    async def create_assistant(self, files_dir: str, name="MyAssistant") -> str:
        file_ids = await self.upload_files(files_dir)
        vector_store = await self.client.beta.vector_stores.create(name="KnowledgeBase")
        for file_id in file_ids:
            await self.client.beta.vector_stores.files.create(
                vector_store_id=vector_store.id,
                file_id=file_id
            )
        assistant = await self.client.beta.assistants.create(
            name=name,
            instructions="Отвечай кратко и по делу. Используй загруженные файлы при необходимости.",
            model="gpt-4-turbo-preview",
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            tools=[{"type": "file_search"}]
        )
        return assistant.id

    async def get_response(self, assistant_id, user_id: int, query: str, message = None, g = None) -> str:
        if user_id not in self.user_threads:
            thread = await self.client.beta.threads.create()
            self.user_threads[user_id] = thread.id
        thread_id = self.user_threads[user_id]
        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=query
        )
        run = await self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        while run.status != "completed":
            if message and g:
                await message.edit_text('Ищу в базе данных: '+ next(g))
            if run.status == "failed":
                return "Ошибка обработки запроса."
            await asyncio.sleep(1)
            run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data[0].content[0].text.value

async def main():
    from config import openai_api_key
    manager = OpenAIAssistantManager(api_key=openai_api_key)
    assistant_id = await manager.create_assistant(files_dir="/path/to/your/files")
    response = await manager.get_response(assistant_id, user_id=1, query="Ваш вопрос")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())