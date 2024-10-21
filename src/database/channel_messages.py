from .database_connection import execute_query
import logging
from typing import List, Tuple, Union
import os

CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))

async def get_messages_for_channel(channel_id: int, user_id: int, limit: int = 50, offset: int = 0, count_only: bool = False) -> Union[List[Tuple], int]:
    logging.debug(f"Attempting to retrieve messages for channel_id={channel_id}, user_id={user_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
                SELECT COUNT(*) 
                FROM messages 
                WHERE channel_id = ? 
                AND (user_id = ? OR user_id = ?)
                AND EXISTS (
                    SELECT 1 
                    FROM messages m2 
                    WHERE m2.channel_id = messages.channel_id 
                    AND m2.user_id = ?
                )
                AND EXISTS (
                    SELECT 1 
                    FROM messages m3 
                    WHERE m3.channel_id = messages.channel_id 
                    AND m3.user_id = ?
                )
            '''
            result = await execute_query(query, (channel_id, user_id, CLIENT_ID, CLIENT_ID, user_id), fetchone=True)
            return result[0] if result else 0
        else:
            query = '''
                SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM messages 
                WHERE channel_id = ? 
                AND (user_id = ? OR user_id = ?)
                AND EXISTS (
                    SELECT 1 
                    FROM messages m2 
                    WHERE m2.channel_id = messages.channel_id 
                    AND m2.user_id = ?
                )
                AND EXISTS (
                    SELECT 1 
                    FROM messages m3 
                    WHERE m3.channel_id = messages.channel_id 
                    AND m3.user_id = ?
                )
                ORDER BY 
                    timestamp ASC
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (channel_id, user_id, CLIENT_ID, CLIENT_ID, user_id, limit, offset))
            logging.debug(f"Retrieved {len(result)} messages for channel {channel_id} and user {user_id}")
            return result
    except Exception as e:
        logging.error(f"Error retrieving messages for channel {channel_id} and user {user_id}: {str(e)}")
        raise
