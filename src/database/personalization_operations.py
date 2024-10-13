from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

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
