from .database_connection import execute_query
import logging
from typing import List, Tuple, Union

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
