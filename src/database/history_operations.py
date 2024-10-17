from typing import List, Tuple, Optional, Any
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
                    timestamp DESC,
                    CASE WHEN message_type = 'user' THEN 1 ELSE 0 END
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (user_id, user_id, limit, offset))
            logging.debug(f"History result for user_id={user_id}: {result}")
            return result
    except Exception as e:
        logging.error(f"Error getting history for user_id={user_id}: {str(e)}")
        return [] if not count_only else 0

async def clear_channel_history(channel_id: int) -> int:
    logging.debug(f"Clearing history for channel_id={channel_id}")
    try:
        # Count messages before deleting
        count_query = 'SELECT COUNT(*) FROM messages WHERE channel_id = ?'
        count_result = await execute_query(count_query, (channel_id,), fetchone=True)
        message_count = count_result[0] if count_result else 0

        # Delete messages
        delete_query = 'DELETE FROM messages WHERE channel_id = ?'
        await execute_query(delete_query, (channel_id,))

        logging.debug(f"Cleared {message_count} messages from channel_id={channel_id}")
        return message_count
    except Exception as e:
        logging.error(f"Error clearing channel history for channel_id={channel_id}: {str(e)}")
        raise

async def clear_user_history() -> int:
    logging.debug("Clearing all user history")
    try:
        messages_count = await execute_query('SELECT COUNT(*) FROM messages', fetchone=True)
        comments_count = await execute_query('SELECT COUNT(*) FROM comments', fetchone=True)
        
        total_rows = messages_count[0] + comments_count[0]
        logging.debug(f"Total rows to delete: {total_rows}")

        await execute_query('DELETE FROM messages')
        logging.debug("Messages table cleared")

        await execute_query('DELETE FROM comments')
        logging.debug("Comments table cleared")

        return total_rows
    except Exception as e:
        logging.error(f"Error clearing user history: {str(e)}")
        raise

async def count_user_history(user_id: int) -> int:
    logging.debug(f"Counting history for user_id={user_id}")
    try:
        count = await get_history(user_id, count_only=True)
        logging.debug(f"Counted history for user_id={user_id}: {count}")
        return count
    except Exception as e:
        logging.error(f"Error counting user history for user_id={user_id}: {str(e)}")
        return 0
