from .database_connection import execute_query
import logging
from typing import List, Tuple, Union
import os

CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))

async def _execute_message_query(query: str, params: tuple, count_only: bool = False) -> Union[List[Tuple], int]:
    """
    Execute a message query and handle common error cases.
    """
    try:
        if count_only:
            result = await execute_query(query, params, fetchone=True)
            return result[0] if result else 0
        else:
            result = await execute_query(query, params)
            return result
    except Exception as e:
        logging.error(f"Error executing message query: {str(e)}")
        raise

async def get_messages_for_channel(channel_id: int, user_id: int, limit: int = 50, offset: int = 0, count_only: bool = False) -> Union[List[Tuple], int]:
    """
    Retrieve messages for a specific channel between a user and the bot.
    """
    logging.debug(f"Attempting to retrieve messages for channel_id={channel_id}, user_id={user_id}, limit={limit}, offset={offset}, count_only={count_only}")
    
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
        params = (channel_id, user_id, CLIENT_ID, CLIENT_ID, user_id)
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
        params = (channel_id, user_id, CLIENT_ID, CLIENT_ID, user_id, limit, offset)

    return await _execute_message_query(query, params, count_only)

async def get_messages_for_user(user_id: int, channel_id: int, limit: int = 50, offset: int = 0, count_only: bool = False) -> Union[List[Tuple], int]:
    """
    Retrieve messages for a specific user, including mentions and bot responses.
    """
    logging.debug(f"Attempting to retrieve messages for user_id={user_id}, channel_id={channel_id}, limit={limit}, offset={offset}, count_only={count_only}")
    
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

    return await _execute_message_query(query, params, count_only)
