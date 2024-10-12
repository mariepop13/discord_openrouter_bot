from typing import List, Tuple, Optional
from .database_connection import execute_query

DEFAULT_AI_MODEL = "google/gemini-flash-1.5"
DEFAULT_MAX_OUTPUT = 150

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
    return await execute_query('''
        SELECT user_id, content, model, message_type, timestamp 
        FROM messages 
        WHERE user_id = ? OR message_type = 'bot' 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (user_id, limit))

async def clear_user_history(user_id: int) -> int:
    result = await execute_query('''
        DELETE FROM messages 
        WHERE user_id = ? OR 
              (message_type = 'bot' AND id IN (
                  SELECT m2.id 
                  FROM messages m2 
                  WHERE m2.message_type = 'bot' AND 
                        m2.timestamp > (
                            SELECT MAX(timestamp) 
                            FROM messages 
                            WHERE user_id = ? AND message_type = 'user'
                        )
              ))
    ''', (user_id, user_id))
    return result.rowcount if hasattr(result, 'rowcount') else 0

async def count_user_history(user_id: int) -> int:
    result = await execute_query('''
        SELECT COUNT(*) 
        FROM messages 
        WHERE user_id = ? OR 
              (message_type = 'bot' AND id IN (
                  SELECT m2.id 
                  FROM messages m2 
                  WHERE m2.message_type = 'bot' AND 
                        m2.timestamp > (
                            SELECT MAX(timestamp) 
                            FROM messages 
                            WHERE user_id = ? AND message_type = 'user'
                        )
              ))
    ''', (user_id, user_id), fetchone=True)
    return result[0] if result else 0
