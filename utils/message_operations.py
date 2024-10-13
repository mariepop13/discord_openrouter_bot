from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

async def insert_message(user_id: int, content: str, model: str, message_type: str) -> None:
    try:
        await execute_query('INSERT INTO messages (user_id, content, model, message_type) VALUES (?, ?, ?, ?)',
                            (user_id, content, model, message_type))
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise
