from typing import Any
from .database_connection import execute_query
import logging

async def get_history(user_id: int, channel_id: int, limit: int = 10, offset: int = 0, count_only: bool = False) -> Any:
    logging.debug(f"Fetching history for user_id={user_id}, channel_id={channel_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
                SELECT COUNT(*) FROM (
                    SELECT id FROM messages
                    WHERE channel_id = ? AND (
                        user_id = ? OR message_type = 'bot'
                    )
                )
            '''
            params = (channel_id, user_id)
            logging.debug(f"Executing count query: {query}")
            logging.debug(f"Query parameters: {params}")
            result = await execute_query(query, params, fetchone=True)
            count = result[0] if result else 0
            logging.debug(f"Count result for user_id={user_id}, channel_id={channel_id}: {count}")
            return count
        else:
            query = '''
                SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM messages
                WHERE channel_id = ? AND (
                    user_id = ? OR message_type = 'bot'
                )
                ORDER BY timestamp ASC
                LIMIT ? OFFSET ?
            '''
            params = (channel_id, user_id, limit, offset)
            logging.debug(f"Executing history query: {query}")
            logging.debug(f"Query parameters: {params}")
            result = await execute_query(query, params)
            logging.debug(f"History result for user_id={user_id}, channel_id={channel_id}: {result}")
            return result
    except Exception as e:
        logging.error(f"Error getting history for user_id={user_id}, channel_id={channel_id}: {str(e)}")
        return [] if not count_only else 0
