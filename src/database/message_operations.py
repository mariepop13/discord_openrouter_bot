from .database_connection import execute_query
import logging
from typing import List, Tuple, Union

async def insert_message(user_id: int, channel_id: int, content: str, model: str, message_type: str, mentioned_user_id: int = None) -> None:
    logging.debug(f"Attempting to insert message: user_id={user_id}, channel_id={channel_id}, content={content}, model={model}, message_type={message_type}, mentioned_user_id={mentioned_user_id}")
    try:
        await execute_query('INSERT INTO messages (user_id, channel_id, content, model, message_type, mentioned_user_id) VALUES (?, ?, ?, ?, ?, ?)',
                            (user_id, channel_id, content, model, message_type, mentioned_user_id))
        logging.debug("Message inserted successfully")
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise

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

async def get_messages_for_user(user_id: int, channel_id: int, limit: int = 50, offset: int = 0, count_only: bool = False) -> Union[List[Tuple], int]:
    logging.debug(f"Attempting to retrieve messages for user_id={user_id}, channel_id={channel_id}, limit={limit}, offset={offset}, count_only={count_only}")
    try:
        if count_only:
            query = '''
                SELECT COUNT(*) FROM (
                    SELECT id FROM messages WHERE user_id = ? AND channel_id = ?
                    UNION ALL
                    SELECT id FROM messages WHERE mentioned_user_id = ? AND channel_id = ?
                    UNION ALL
                    SELECT m.id
                    FROM messages m
                    JOIN messages um ON m.timestamp > um.timestamp
                    WHERE um.user_id = ? AND um.channel_id = ? AND m.channel_id = ? AND m.message_type = 'bot'
                    AND m.timestamp <= (
                        SELECT MIN(timestamp)
                        FROM messages
                        WHERE timestamp > um.timestamp AND channel_id = ? AND user_id != m.user_id
                    )
                )
            '''
            params = (user_id, channel_id, user_id, channel_id, user_id, channel_id, channel_id, channel_id)
            
            result = await execute_query(query, params, fetchone=True)
            return result[0] if result else 0
        else:
            query = '''
                WITH user_messages AS (
                    SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                    FROM messages
                    WHERE (user_id = ? OR mentioned_user_id = ?) AND channel_id = ?
                    ORDER BY timestamp ASC
                    LIMIT ? OFFSET ?
                )
                SELECT user_id, content, model, message_type, timestamp, mentioned_user_id
                FROM (
                    SELECT user_id, content, model, message_type, timestamp, mentioned_user_id FROM user_messages
                    UNION ALL
                    SELECT m.user_id, m.content, m.model, m.message_type, m.timestamp, m.mentioned_user_id
                    FROM messages m
                    JOIN user_messages um ON m.timestamp > um.timestamp
                    WHERE m.channel_id = ? AND m.message_type = 'bot'
                    AND m.timestamp <= (
                        SELECT MIN(timestamp)
                        FROM messages
                        WHERE timestamp > um.timestamp AND channel_id = ? AND user_id != m.user_id
                    )
                )
                ORDER BY timestamp ASC
            '''
            params = (user_id, user_id, channel_id, limit, offset, channel_id, channel_id)

            result = await execute_query(query, params)
            logging.debug(f"Retrieved {len(result)} messages for user {user_id} in channel {channel_id}")
            return result
    except Exception as e:
        logging.error(f"Error retrieving messages for user {user_id} in channel {channel_id}: {str(e)}")
        raise

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
