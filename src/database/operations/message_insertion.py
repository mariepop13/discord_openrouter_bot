from src.database.schema.database_connection import execute_query
import logging

async def insert_message(user_id: int, channel_id: int, content: str, model: str, message_type: str, mentioned_user_id: int = None) -> None:
    logging.debug(f"Attempting to insert message: user_id={user_id}, channel_id={channel_id}, content={content}, model={model}, message_type={message_type}, mentioned_user_id={mentioned_user_id}")
    try:
        await execute_query('INSERT INTO messages (user_id, channel_id, content, model, message_type, mentioned_user_id) VALUES (?, ?, ?, ?, ?, ?)',
                            (user_id, channel_id, content, model, message_type, mentioned_user_id))
        logging.debug("Message inserted successfully")
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise
