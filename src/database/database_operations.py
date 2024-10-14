import logging
from .message_operations import insert_message
from .personalization_operations import get_personalization, set_personalization
from .ai_preferences_operations import get_ai_preferences, set_ai_preferences, DEFAULT_AI_MODEL, DEFAULT_MAX_OUTPUT
from .history_operations import get_history, clear_user_history, count_user_history

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
logger.info("Database operations module loaded successfully.")
