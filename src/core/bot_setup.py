import asyncio
import logging
from src.core.bot_initialization import initialize_bot
from src.core.command_registration import register_commands
from src.database.database_schema import setup_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_bot():
    logger.info("Setting up bot in bot_setup.py...")
    
    # Initialize the bot
    bot = initialize_bot()
    logger.info("Bot initialized.")
    
    # Register slash commands
    register_commands(bot)
    logger.info("Commands registered.")
    
    # Setup the database
    asyncio.run(setup_database())
    logger.info("Database setup completed.")
    
    logger.info("Bot setup completed in bot_setup.py")
    return bot
