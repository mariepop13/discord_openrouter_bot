from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

async def get_personalization(user_id: int) -> Optional[Tuple[Any, ...]]:
    logging.info(f"Fetching personalization for user_id: {user_id}")
    try:
        result = await execute_query('SELECT personality, tone, language, ai_model, max_output FROM personalization WHERE user_id = ?',
                                     (user_id,), fetchone=True)
        logging.info(f"Personalization fetched for user_id: {user_id}, result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error getting personalization for user_id {user_id}: {str(e)}")
        return None

async def set_personalization(user_id: int, field: str, value: str) -> None:
    logging.info(f"Setting personalization for user_id: {user_id}, field: {field}, value: {value}")
    try:
        await execute_query(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)',
                            (user_id, value))
        logging.info(f"Personalization set for user_id: {user_id}, field: {field}, value: {value}")
    except Exception as e:
        logging.error(f"Error setting personalization for user_id {user_id}, field: {field}, value: {value}: {str(e)}")
        raise
