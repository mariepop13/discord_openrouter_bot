from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

DEFAULT_AI_MODEL = "google/gemini-flash-1.5"
DEFAULT_MAX_OUTPUT = 150

logging.basicConfig(level=logging.DEBUG)

async def get_ai_preferences(user_id: int) -> Tuple[str, int]:
    logging.debug(f"Fetching AI preferences for user_id: {user_id}")
    try:
        result = await execute_query('SELECT ai_model, max_output FROM personalization WHERE user_id = ?',
                                     (user_id,), fetchone=True)
        if result:
            logging.debug(f"AI preferences found for user_id {user_id}: {result}")
        else:
            logging.debug(f"No AI preferences found for user_id {user_id}, using defaults.")
        return result if result else (DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT)
    except Exception as e:
        logging.error(f"Error getting AI preferences for user_id {user_id}: {str(e)}")
        return DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT

async def set_ai_preferences(user_id: int, ai_model: Optional[str] = None, max_output: Optional[int] = None) -> None:
    logging.debug(f"Setting AI preferences for user_id: {user_id}, ai_model: {ai_model}, max_output: {max_output}")
    try:
        await execute_query('INSERT OR REPLACE INTO personalization (user_id, ai_model, max_output) VALUES (?, ?, ?)',
                            (user_id, ai_model, max_output))
        logging.debug(f"AI preferences set for user_id {user_id}")
    except Exception as e:
        logging.error(f"Error setting AI preferences for user_id {user_id}: {str(e)}")
        raise
