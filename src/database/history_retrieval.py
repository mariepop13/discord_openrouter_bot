from typing import Any
from .database_connection import execute_query
import logging

async def get_history(user_id: int, channel_id: int, limit: int = 10, offset: int = 0, count_only: bool = False) -> Any:
    logging.debug(f"Fetching history for user_id={user_id}, channel_id={channel_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
                SELECT COUNT(DISTINCT id) FROM (
                    SELECT id FROM messages
                    WHERE user_id = ? AND channel_id = ?
                    UNION
                    SELECT id FROM messages
                    WHERE message_type = 'bot' AND channel_id = ? AND mentioned_user_id = ?
                )
            '''
            result = await execute_query(query, (user_id, channel_id, channel_id, user_id), fetchone=True)
            count = result[0] if result else 0
            logging.debug(f"Count result for user_id={user_id}, channel_id={channel_id}: {count}")
            return count
        else:
            query = '''
                SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM (
                    SELECT * FROM messages
                    WHERE user_id = ? AND channel_id = ?
                    UNION ALL
                    SELECT *
                    FROM messages
                    WHERE message_type = 'bot' AND channel_id = ? AND mentioned_user_id = ?
                )
                ORDER BY timestamp ASC
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (user_id, channel_id, channel_id, user_id, limit, offset))
            logging.debug(f"History result for user_id={user_id}, channel_id={channel_id}: {result}")
            return result
    except Exception as e:
        logging.error(f"Error getting history for user_id={user_id}, channel_id={channel_id}: {str(e)}")
        return [] if not count_only else 0
