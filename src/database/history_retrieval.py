from typing import Any
from .database_connection import execute_query
import logging

async def get_history(user_id: int, limit: int = 10, offset: int = 0, count_only: bool = False) -> Any:
    logging.debug(f"Fetching history for user_id={user_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
                SELECT COUNT(DISTINCT id) FROM (
                    SELECT id FROM messages
                    WHERE user_id = ? OR mentioned_user_id = ?
                    UNION
                    SELECT m.id
                    FROM messages m
                    JOIN messages u ON m.timestamp > u.timestamp
                    WHERE u.user_id = ? AND m.message_type = 'bot'
                    AND m.timestamp <= (
                        SELECT MIN(timestamp)
                        FROM messages
                        WHERE timestamp > u.timestamp AND user_id != ?
                    )
                )
            '''
            result = await execute_query(query, (user_id, user_id, user_id, user_id), fetchone=True)
            count = result[0] if result else 0
            logging.debug(f"Count result for user_id={user_id}: {count}")
            return count
        else:
            query = '''
                SELECT DISTINCT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM (
                    SELECT * FROM messages
                    WHERE user_id = ? OR mentioned_user_id = ?
                    UNION
                    SELECT m.*
                    FROM messages m
                    JOIN messages u ON m.timestamp > u.timestamp
                    WHERE u.user_id = ? AND m.message_type = 'bot'
                    AND m.timestamp <= (
                        SELECT MIN(timestamp)
                        FROM messages
                        WHERE timestamp > u.timestamp AND user_id != ?
                    )
                )
                ORDER BY timestamp ASC
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (user_id, user_id, user_id, user_id, limit, offset))
            logging.debug(f"History result for user_id={user_id}: {result}")
            return result
    except Exception as e:
        logging.error(f"Error getting history for user_id={user_id}: {str(e)}")
        return [] if not count_only else 0
