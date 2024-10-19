from .database_connection import execute_query
import logging
from typing import Tuple

async def get_last_message_for_channel(channel_id: int) -> Tuple:
    logging.debug(f"Attempting to retrieve last message for channel_id={channel_id}")
    try:
        result = await execute_query('''
            SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
            FROM messages 
            WHERE channel_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (channel_id,))
        if result:
            logging.debug(f"Retrieved last message for channel {channel_id}")
            return result[0]
        else:
            logging.debug(f"No messages found for channel {channel_id}")
            return None
    except Exception as e:
        logging.error(f"Error retrieving last message for channel {channel_id}: {str(e)}")
        raise
