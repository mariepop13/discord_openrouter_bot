import discord
from discord import Interaction
import logging
from src.database.operations.database_operations import clear_user_history
from src.utils.chat.message_utils import send_message

logger = logging.getLogger(__name__)

async def clear_command(interaction: Interaction):
    """Clear all conversation history for a user."""
    logger.debug("Clear command received")
    try:
        rows_deleted = await clear_user_history()
        response_message = f"All conversation history has been cleared. {rows_deleted} entries have been deleted."
        await send_message(interaction, response_message)
        logger.debug(f"Clear command successful: {rows_deleted} entries deleted")
    except Exception as e:
        logging.error(f"Error in clear command: {str(e)}")
        await send_message(
            interaction, 
            "An error occurred while clearing the conversation history. Please try again later."
        )
        logger.error("Clear command failed")

async def purge_command(interaction: Interaction, amount: int = None):
    """Purge a specified number of messages from a channel."""
    logger.debug(f"Purge command received with amount: {amount}")
    try:
        await interaction.response.defer(ephemeral=True)
        
        if amount is None:
            deleted = await interaction.channel.purge(limit=None)
            logger.info(f"All messages purged from the channel")
        else:
            deleted = await interaction.channel.purge(limit=amount)
            logger.info(f"{len(deleted)} messages purged from the channel")
        
        await interaction.followup.send(
            f"{len(deleted)} message(s) have been deleted.", 
            ephemeral=True
        )
    except discord.errors.Forbidden:
        await interaction.followup.send(
            "I don't have the required permissions to delete messages. "
            "Please make sure I have the 'Manage Messages' permission in this channel.",
            ephemeral=True
        )
        logger.error("Purge command failed due to insufficient permissions")
    except Exception as e:
        await interaction.followup.send(
            "An error occurred while trying to delete messages.",
            ephemeral=True
        )
        logger.error(f"Error in purge command: {str(e)}")
