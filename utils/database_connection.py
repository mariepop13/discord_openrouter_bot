import sqlite3
from contextlib import asynccontextmanager

DATABASE_NAME = 'bot_database.sqlite'

@asynccontextmanager
async def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()

async def execute_query(query: str, params: tuple = (), fetchone: bool = False):
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise
