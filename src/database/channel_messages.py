from .database_connection import execute_query
import logging
from typing import List, Tuple, Union

async def get_messages_for_channel(channel_id: int, limit: int = 50, offset: int = 0, count_only: bool = False) -> Union[List[Tuple], int]:
    logging.debug(f"Attempting to retrieve messages for channel_id={channel_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = 'SELECT COUNT(*) FROM messages WHERE channel_id = ?'
            result = await execute_query(query, (channel_id,), fetchone=True)
            return result[0] if result else 0
        else:
            query = '''
                SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM messages 
                WHERE channel_id = ? 
                ORDER BY 
                    timestamp ASC,
                    CASE WHEN message_type = 'bot' THEN 1 ELSE 0 END
                LIMIT ? OFFSET ?
            '''
            result = await execute_query(query, (channel_id, limit, offset))
            logging.debug(f"Retrieved {len(result)} messages for channel {channel_id}")
            return result
    except Exception as e:
        logging.error(f"Error retrieving messages for channel {channel_id}: {str(e)}")
        raise
