import os
import asyncio
from discord import errors
from src.utils.logging.logging_utils import get_logger

logger = get_logger(__name__)

async def attempt_reconnect(bot, max_retries=5, delay=5):
    """Attempts to reconnect the bot to Discord after a connection failure."""
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
