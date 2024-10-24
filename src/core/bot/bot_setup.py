import asyncio
import logging
from src.core.bot.bot_initialization import initialize_bot
from src.core.handlers.command_registration import register_commands
from src.database.schema.database_schema import setup_database

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
    
    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.name}")
        logger.info("Syncing commands...")
        await bot.tree.sync()
        logger.info("Commands synced successfully.")
    
    logger.debug("Bot setup completed in bot_setup.py")
    return bot
