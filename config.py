from dotenv import load_dotenv
import os
import logging

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных окружения
openai_api_key = os.getenv('OPENAI_API_KEY')
telegram_bot_token = os.getenv('telegram_bot_token')
knowledge_base_path = os.getenv('knowledge_base_path')
DATABASE = os.getenv('db_path')
assistant_id = 'asst_UyP56aVaVRpdHu6iwtCJkjtj'
admins = [149378045]

with open(knowledge_base_path, 'r', encoding='utf-8') as file:
    knowledge_base_promt = file.read()


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Пример использования логирования
logging.info('Конфигурация загружена успешно')