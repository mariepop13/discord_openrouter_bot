from .database_connection import execute_query
import logging

async def insert_message(user_id: int, content: str, model: str, message_type: str) -> None:
    logging.info(f"Attempting to insert message: user_id={user_id}, content={content}, model={model}, message_type={message_type}")
    try:
        await execute_query('INSERT INTO messages (user_id, content, model, message_type) VALUES (?, ?, ?, ?)',
                            (user_id, content, model, message_type))
        logging.info("Message inserted successfully")
    except Exception as e:
        logging.error(f"Error inserting message: {str(e)}")
        raise
