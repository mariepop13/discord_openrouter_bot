import sqlite3
import logging
from contextlib import asynccontextmanager
from typing import List, Tuple, Optional, Any

DATABASE_NAME = 'bot_database.sqlite'
DEFAULT_AI_MODEL = "google/gemini-flash-1.5"
DEFAULT_MAX_OUTPUT = 150

@asynccontextmanager
async def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()

async def setup_database():
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        
        await create_tables(cursor)
        await run_migrations(cursor)
        
        conn.commit()

async def create_tables(cursor: sqlite3.Cursor):
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            model TEXT,
            message_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS personalization (
            user_id INTEGER PRIMARY KEY,
            personality TEXT,
            tone TEXT,
            language TEXT,
            ai_model TEXT,
            max_output INTEGER
        );
    ''')

async def run_migrations(cursor: sqlite3.Cursor):
    migrations = {
        'personalization': ['ai_model', 'max_output'],
        'messages': ['message_type']
    }
    
    for table, new_columns in migrations.items():
        existing_columns = await get_existing_columns(cursor, table)
        for column in new_columns:
            if column not in existing_columns:
                logging.info(f"Adding {column} column to {table} table")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")

async def get_existing_columns(cursor: sqlite3.Cursor, table: str) -> List[str]:
    cursor.execute(f"PRAGMA table_info({table})")
    return [column[1] for column in cursor.fetchall()]

async def execute_query(query: str, params: Tuple = (), fetchone: bool = False) -> Any:
    async with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            raise

async def insert_message(user_id: int, content: str, model: str, message_type: str):
    await execute_query('INSERT INTO messages (user_id, content, model, message_type) VALUES (?, ?, ?, ?)',
                        (user_id, content, model, message_type))

async def get_personalization(user_id: int) -> Optional[Tuple]:
    return await execute_query('SELECT personality, tone, language, ai_model, max_output FROM personalization WHERE user_id = ?',
                               (user_id,), fetchone=True)

async def set_personalization(user_id: int, field: str, value: str):
    await execute_query(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)',
                        (user_id, value))

async def get_ai_preferences(user_id: int) -> Tuple[str, int]:
    result = await execute_query('SELECT ai_model, max_output FROM personalization WHERE user_id = ?',
                                 (user_id,), fetchone=True)
    return result if result else (DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT)

async def set_ai_preferences(user_id: int, ai_model: Optional[str] = None, max_output: Optional[int] = None):
    await execute_query('INSERT OR REPLACE INTO personalization (user_id, ai_model, max_output) VALUES (?, ?, ?)',
                        (user_id, ai_model, max_output))

async def get_history(user_id: int, limit: int) -> List[Tuple]:
    return await execute_query('SELECT content, model, message_type, timestamp FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
                               (user_id, limit))

async def clear_user_history(user_id: int) -> int:
    result = await execute_query('DELETE FROM messages WHERE user_id = ?', (user_id,))
    return result.rowcount if result else 0
