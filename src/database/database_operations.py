from src.utils.logging_utils import get_logger
from .message_operations import insert_message
from .personalization_operations import get_personalization, set_personalization
from .ai_preferences_operations import get_ai_preferences, set_ai_preferences, DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT
from .history_retrieval import get_history
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
    'DEFAULT_AI_MODEL',
    'DEFAULT_MAX_OUTPUT',
    'get_history',
    'clear_user_history',
    'count_user_history'
]

# Example of logging usage
logger.debug("Database operations module loaded successfully.")
