from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
from config import DEFAULT_CHAT_MODEL, DEFAULT_MAX_OUTPUT
import logging

async def get_personalization(user_id: int, fields: Optional[List[str]] = None) -> Tuple[Any, ...]:
    """
    Get personalization settings for a user.
    If fields is None, fetches all fields.
    Returns defaults for AI-specific fields if not set.
    """
    try:
        field_list = ', '.join(fields) if fields else 'personality, tone, language, ai_model, max_output'
        result = await execute_query(f'SELECT {field_list} FROM personalization WHERE user_id = ?',
                                   (user_id,), fetchone=True)
        
        # Handle defaults for AI-specific fields if they were requested
        if result is None and fields:
            if 'ai_model' in fields and 'max_output' in fields:
                return (DEFAULT_CHAT_MODEL, DEFAULT_MAX_OUTPUT)
            elif 'ai_model' in fields:
                return (DEFAULT_CHAT_MODEL,)
            elif 'max_output' in fields:
                return (DEFAULT_MAX_OUTPUT,)
        
        return result
    except Exception as e:
        logging.error(f"Error getting personalization for user_id {user_id}: {str(e)}")
        return None

async def set_personalization(user_id: int, field: str, value: Any) -> None:
    """Set a single personalization field for a user."""
    try:
        await execute_query(f'INSERT OR REPLACE INTO personalization (user_id, {field}) VALUES (?, ?)',
                          (user_id, value))
    except Exception as e:
        logging.error(f"Error setting personalization for user_id {user_id}, field: {field}: {str(e)}")
        raise

# Convenience methods for AI preferences
async def get_ai_preferences(user_id: int) -> Tuple[str, int]:
    """Get AI-specific preferences with defaults."""
    result = await get_personalization(user_id, ['ai_model', 'max_output'])
    return result if result else (DEFAULT_CHAT_MODEL, DEFAULT_MAX_OUTPUT)

async def set_ai_preferences(user_id: int, ai_model: Optional[str] = None, max_output: Optional[int] = None) -> None:
    """Set AI-specific preferences."""
    if ai_model is not None:
        await set_personalization(user_id, 'ai_model', ai_model)
    if max_output is not None:
        await set_personalization(user_id, 'max_output', max_output)
