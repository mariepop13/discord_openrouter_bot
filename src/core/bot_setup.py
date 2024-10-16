import asyncio
import logging
from src.core.bot_initialization import initialize_bot
from src.core.command_registration import register_commands
from src.database.database_schema import setup_database

# Get logger
logger = logging.getLogger(__name__)

def setup_bot():
    logger.debug("Setting up bot in bot_setup.py...")
    
    # Initialize the bot
    bot = initialize_bot()
    logger.debug("Bot initialized.")
    
    # Register slash commands
    register_commands(bot)
    logger.debug("Commands registered.")
    
    # Setup the database
    asyncio.run(setup_database())
    logger.debug("Database setup completed.")
    
    logger.debug("Bot setup completed in bot_setup.py")
    return bot
