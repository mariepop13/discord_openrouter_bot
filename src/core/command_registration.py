import logging
from src.core.ai_commands import register_ai_commands
from src.core.image_commands import register_image_commands
from src.core.clear_command import register_clear_command
from src.core.utility_commands import register_utility_commands
from src.commands.history_command import register_history_command

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_commands(bot):
    register_ai_commands(bot)
    register_image_commands(bot)
    register_clear_command(bot)
    register_utility_commands(bot)
    register_history_command(bot)

    logger.info("All commands registered successfully.")
