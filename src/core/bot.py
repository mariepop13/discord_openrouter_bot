import os
import asyncio
from dotenv import load_dotenv
from discord import errors, Intents
from discord.ext import commands
from src.core.bot_initialization import initialize_bot
from src.core.command_registration import register_commands
from src.core.event_handlers import setup_event_handlers
from src.core.connection_manager import attempt_reconnect
from src.utils.logging_utils import get_logger
from src.commands.history_command import register_history_command
from src.database.database_schema import setup_database

logger = get_logger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded.")

async def setup_bot():
    """Initialize and configure the bot with all necessary components."""
    bot = initialize_bot()
    bot.command_prefix = '!'
    logger.debug("Bot initialized.")

    # Set up the database
    await setup_database()
    logger.debug("Database setup completed.")

    # Register commands and event handlers
    register_commands(bot)
    register_history_command(bot)
    setup_event_handlers(bot)
    logger.debug("Commands and event handlers registered.")

    return bot

async def run_bot():
    """Main function to run the bot with automatic reconnection handling."""
    bot = await setup_bot()
    logger.debug("Starting the bot.")
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        logger.error("DISCORD_TOKEN not found in .env file")
        return

    while True:
        try:
            await bot.start(token)
        except errors.ConnectionClosed:
            logger.warning("Connection closed. Attempting to reconnect...")
            if not await attempt_reconnect(bot):
                logger.error("Failed to reconnect after multiple attempts. Exiting.")
                break
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break
    
    logger.debug("Bot has stopped running.")

if __name__ == "__main__":
    asyncio.run(run_bot())
