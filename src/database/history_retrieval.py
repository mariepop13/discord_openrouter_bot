from typing import Any
from .database_connection import execute_query
import logging

async def get_history(user_id: int, limit: int = 10, offset: int = 0, count_only: bool = False) -> Any:
    logging.debug(f"Fetching history for user_id={user_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
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
            '''
            result = await execute_query(query, (user_id, user_id), fetchone=True)
            count = result[0] if result else 0
            logging.debug(f"Count result for user_id={user_id}: {count}")
            return count
        else:
            query = '''
                SELECT user_id, content, model, message_type, timestamp 
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
                ORDER BY 
                    timestamp ASC,
                    CASE WHEN message_type = 'bot' THEN 1 ELSE 0 END
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (user_id, user_id, limit, offset))
            logging.debug(f"History result for user_id={user_id}: {result}")
            return result
    except Exception as e:
        logging.error(f"Error getting history for user_id={user_id}: {str(e)}")
        return [] if not count_only else 0
