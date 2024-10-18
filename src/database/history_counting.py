import logging
from .history_retrieval import get_history

async def count_user_history(user_id: int) -> int:
    logging.debug(f"Counting history for user_id={user_id}")
    try:
        count = await get_history(user_id, count_only=True)
        logging.debug(f"Counted history for user_id={user_id}: {count}")
        return count
    except Exception as e:
        logging.error(f"Error counting user history for user_id={user_id}: {str(e)}")
        return 0
