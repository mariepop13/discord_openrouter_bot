import os
from src.utils.logging.logging_utils import get_logger
from src.utils.logging.log_cleanup import cleanup_logs
from src.core.bot.bot_config import create_bot, generate_invite_link
from src.core.handlers.event_handlers import setup_event_handlers
from src.core.handlers.sync_commands import setup_sync_command

logger = get_logger(__name__)

def initialize_bot():
    """Initialize the Discord bot with all necessary configurations and handlers."""
    logger.debug("Initializing bot...")
    
    # Clean up log files
    log_files_to_keep = int(os.getenv('LOG_FILES_TO_KEEP', 5))
    logger.info(f"Cleaning up log files, keeping the {log_files_to_keep} most recent files.")
    cleanup_logs(keep_latest=log_files_to_keep)
    logger.info("Log cleanup completed.")
    
    # Create and configure the bot
    bot = create_bot()
    
    # Generate invite link
    generate_invite_link(bot)
    
    # Set up event handlers
    setup_event_handlers(bot)
    
    # Set up sync command
    setup_sync_command(bot)
    
    return bot
