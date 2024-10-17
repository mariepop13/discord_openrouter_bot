from .database_connection import execute_query
import logging
from typing import List, Tuple

async def insert_message(user_id: int, channel_id: int, content: str, model: str, message_type: str) -> None:
    logging.debug(f"Attempting to insert message: user_id={user_id}, channel_id={channel_id}, content={content}, model={model}, message_type={message_type}")
    try:
        await execute_query('INSERT INTO messages (user_id, channel_id, content, model, message_type) VALUES (?, ?, ?, ?, ?)',
                            (user_id, channel_id, content, model, message_type))
        logging.debug("Message inserted successfully")
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise

async def get_messages_for_channel(channel_id: int, limit: int = 50) -> List[Tuple]:
    logging.debug(f"Attempting to retrieve messages for channel_id={channel_id}, limit={limit}")
    try:
        result = await execute_query('''
            SELECT user_id, content, model, message_type, timestamp 
            FROM messages 
            WHERE channel_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (channel_id, limit))
        logging.debug(f"Retrieved {len(result)} messages for channel {channel_id}")
        return result
    except Exception as e:
        logging.error(f"Error retrieving messages for channel {channel_id}: {str(e)}")
        raise

async def get_last_message_for_channel(channel_id: int) -> Tuple:
    logging.debug(f"Attempting to retrieve last message for channel_id={channel_id}")
    try:
        result = await execute_query('''
            SELECT user_id, content, model, message_type, timestamp 
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
