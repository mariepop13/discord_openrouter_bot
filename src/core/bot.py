import os
import asyncio
from dotenv import load_dotenv
from discord import errors
from discord.ext import commands
from src.core.bot_initialization import initialize_bot
from src.core.command_registration import register_commands
from src.utils.logging_utils import get_logger
from src.commands.history_command import register_history_command
from src.database.database_schema import setup_database

# Configure logging
logger = get_logger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded.")

async def setup_bot():
    # Initialize the bot with command prefix
    bot = initialize_bot()
    bot.command_prefix = '!'
    logger.debug("Bot initialized.")

    # Set up the database
    await setup_database()
    logger.debug("Database setup completed.")

    # Register commands
    register_commands(bot)
    logger.debug("Commands registered.")

    # Register the history command
    register_history_command(bot)
    logger.debug("History command registered.")

    @bot.event
    async def on_error(event, *args, **kwargs):
        logger.error(f"An error occurred in event {event}: {args[0]}")
        if isinstance(args[0], errors.ConnectionClosed):
            logger.warning("Connection closed. Attempting to reconnect...")
            await attempt_reconnect(bot)

    return bot

async def attempt_reconnect(bot, max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            logger.info(f"Reconnection attempt {attempt + 1}/{max_retries}")
            await bot.login(os.getenv('DISCORD_TOKEN'))
            await bot.connect()
            logger.info("Reconnection successful")
            return True
        except errors.ConnectionClosed:
            logger.warning(f"Reconnection attempt {attempt + 1} failed. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    
    logger.error(f"Failed to reconnect after {max_retries} attempts. Please check your internet connection and Discord's status.")
    return False

async def run_bot():
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
