from typing import List, Tuple, Optional, Any
from .database_connection import execute_query
import logging

async def get_history(user_id: int, limit: int = 10, offset: int = 0, count_only: bool = False) -> Any:
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
            return result[0] if result else 0
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
            return await execute_query(query, (user_id, user_id, limit, offset))
    except Exception as e:
        logging.error(f"Error getting history: {str(e)}")
        return [] if not count_only else 0

async def clear_user_history() -> int:
    try:
        # Count rows before deletion
        messages_count = await execute_query('SELECT COUNT(*) FROM messages', fetchone=True)
        comments_count = await execute_query('SELECT COUNT(*) FROM comments', fetchone=True)
        
        total_rows = messages_count[0] + comments_count[0]

        # Clear messages table
        await execute_query('DELETE FROM messages')

        # Clear comments table
        await execute_query('DELETE FROM comments')

        return total_rows
    except Exception as e:
        logging.error(f"Error clearing user history: {str(e)}")
        raise

async def count_user_history(user_id: int) -> int:
    try:
        return await get_history(user_id, count_only=True)
    except Exception as e:
        logging.error(f"Error counting user history: {str(e)}")
        return 0
