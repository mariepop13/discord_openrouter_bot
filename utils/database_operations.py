from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

DEFAULT_AI_MODEL = "google/gemini-flash-1.5"
DEFAULT_MAX_OUTPUT = 150

async def insert_message(user_id: int, content: str, model: str, message_type: str) -> None:
    try:
        await execute_query('INSERT INTO messages (user_id, content, model, message_type) VALUES (?, ?, ?, ?)',
                            (user_id, content, model, message_type))
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise

async def get_personalization(user_id: int) -> Optional[Tuple[Any, ...]]:
    try:
        return await execute_query('SELECT personality, tone, language, ai_model, max_output FROM personalization WHERE user_id = ?',
                                   (user_id,), fetchone=True)
    except Exception as e:
        logging.error(f"Error getting personalization: {str(e)}")
        return None

async def set_personalization(user_id: int, field: str, value: str) -> None:
    try:
        await execute_query(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)',
                            (user_id, value))
    except Exception as e:
        logging.error(f"Error setting personalization: {str(e)}")
        raise

async def get_ai_preferences(user_id: int) -> Tuple[str, int]:
    try:
        result = await execute_query('SELECT ai_model, max_output FROM personalization WHERE user_id = ?',
                                     (user_id,), fetchone=True)
        return result if result else (DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT)
    except Exception as e:
        logging.error(f"Error getting AI preferences: {str(e)}")
        return DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT

async def set_ai_preferences(user_id: int, ai_model: Optional[str] = None, max_output: Optional[int] = None) -> None:
    try:
        await execute_query('INSERT OR REPLACE INTO personalization (user_id, ai_model, max_output) VALUES (?, ?, ?)',
                            (user_id, ai_model, max_output))
    except Exception as e:
        logging.error(f"Error setting AI preferences: {str(e)}")
        raise

async def get_history(user_id: int, limit: int) -> List[Tuple[Any, ...]]:
    try:
        return await execute_query('''
            SELECT user_id, content, model, message_type, timestamp 
            FROM messages 
            WHERE user_id = ? OR message_type = 'bot' 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
    except Exception as e:
        logging.error(f"Error getting history: {str(e)}")
        return []

async def clear_user_history() -> int:
    try:
        # Count rows before deletion
        messages_count = await execute_query('SELECT COUNT(*) FROM messages', fetchone=True)
        comments_count = await execute_query('SELECT COUNT(*) FROM comments', fetchone=True)
        
        total_rows = messages_count[0] + comments_count[0]

        # Clear messages table
        await execute_query('DELETE FROM messages')

        # Clear comments table
        await execute_query('DELETE FROM comments')

        return total_rows
    except Exception as e:
        logging.error(f"Error clearing user history: {str(e)}")
        raise

async def count_user_history(user_id: int) -> int:
    try:
        result = await execute_query('''
            SELECT COUNT(*) 
            FROM messages 
            WHERE user_id = ? OR 
                  (message_type = 'bot' AND id IN (
                      SELECT m2.id 
                      FROM messages m2 
                      WHERE m2.message_type = 'bot' AND 
                            m2.timestamp >= (
                                SELECT MIN(timestamp) 
                                FROM messages 
                                WHERE user_id = ? AND message_type = 'user'
                            )
                  ))
        ''', (user_id, user_id), fetchone=True)
        return result[0] if result else 0
    except Exception as e:
        logging.error(f"Error counting user history: {str(e)}")
        return 0
