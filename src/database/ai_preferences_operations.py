from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

DEFAULT_AI_MODEL = "google/gemini-flash-1.5"
DEFAULT_MAX_OUTPUT = 150

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
