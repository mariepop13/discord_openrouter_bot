from src.utils.logging.logging_utils import get_logger
from src.database.operations.message_operations import insert_message
from .personalization_operations import get_personalization, set_personalization, get_ai_preferences, set_ai_preferences
from config import DEFAULT_CHAT_MODEL, DEFAULT_MAX_OUTPUT
from src.database.operations.history_retrieval import get_history
from .history_clearing import clear_user_history
from .history_counting import count_user_history

# Use our custom logger
logger = get_logger(__name__)

__all__ = [
    'insert_message',
    'get_personalization',
    'set_personalization',
    'get_ai_preferences',
    'set_ai_preferences',
    'DEFAULT_CHAT_MODEL',
    'DEFAULT_MAX_OUTPUT',
    'get_history',
    'clear_user_history',
    'count_user_history'
]

# Example of logging usage
logger.debug("Database operations module loaded successfully.")