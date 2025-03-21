import aiosqlite
from models.models import QueryResponse
from config import DATABASE

print(DATABASE)

async def create_table():
    try:
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS query_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    answer TEXT NOT NULL
                )
            ''')
            await db.commit()
    except Exception as e:
        print(f"Error creating table: {e}")

async def insert_query_response(query_response: QueryResponse):
    try:
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('''
                INSERT INTO query_responses (query, answer)
                VALUES (?, ?)
            ''', (query_response.query, query_response.answer))
            print(1)
            await db.commit()
    except Exception as e:
        print(f"Error inserting query response: {e}")

async def get_query_response(query_id: int) -> QueryResponse:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute('''
                SELECT id, query, answer
                FROM query_responses
                WHERE id = ?
            ''', (query_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return QueryResponse(id=row[0], query=row[1], answer=row[2])
                return None
    except Exception as e:
        print(f"Error getting query response: {e}")

# Example usage
async def main():
    await create_table()
    query_response = QueryResponse(query="What is AI?", answer="AI stands for Artificial Intelligence.")
    await insert_query_response(query_response)
    retrieved_response = await get_query_response(1)
    print(retrieved_response)