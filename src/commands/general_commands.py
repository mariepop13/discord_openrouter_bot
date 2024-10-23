import logging
from discord import Interaction
from src.utils.message_utils import send_message
from .help_content import create_help_embed
from .moderation_commands import clear_command, purge_command

logger = logging.getLogger(__name__)

async def ping(interaction: Interaction):
    """Simple ping command to check bot responsiveness."""
    logger.debug("Ping command received")
    await send_message(interaction, 'Pong!', ephemeral=False)

async def help_command(interaction: Interaction):
    """Display help information about the bot and its commands."""
    logger.debug("Help command received")
    help_embed = create_help_embed()
    await send_message(interaction, content="", embed=help_embed, ephemeral=False)
    logger.debug("Help message sent")

async def clear(interaction: Interaction):
    """Clear user conversation history."""
    await clear_command(interaction)

async def purge(interaction: Interaction, amount: int = None):
    """Purge messages from a channel."""
    await purge_command(interaction, amount)
