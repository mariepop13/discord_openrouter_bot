from .database_connection import execute_query
import logging

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