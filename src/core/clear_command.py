import discord
from discord import app_commands
from src.database.history_clearing import clear_channel_history
from src.database.history_clearing import clear_user_history
from src.utils.history_utils import get_channel_choices
from typing import Optional, Literal, List
import logging

logger = logging.getLogger(__name__)

def register_clear_command(bot):
    @bot.tree.command(name="clear", description="Clear messages from a channel")
    @app_commands.describe(
        target="Choose where to clear messages from",
        channel="The channel to clear messages from (if 'other' is selected)"
    )
    async def clear_command(
        interaction: discord.Interaction,
        target: Literal["current", "other", "all"],
        channel: Optional[str] = None
    ):
        logger.debug(f"Received /clear command with target: {target}, channel: {channel}")
        
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to clear messages.", ephemeral=True)
            return

        try:
            if target == "current":
                deleted = await clear_channel_history(interaction.channel.id)
                await interaction.response.send_message(f"Cleared {deleted} messages from the current channel.", ephemeral=True)
            elif target == "other":
                if channel is None:
                    await interaction.response.send_message("You must specify a channel when selecting 'other'.", ephemeral=True)
                    return
                channel_id = int(channel)
                target_channel = interaction.guild.get_channel(channel_id)
                if target_channel is None:
                    await interaction.response.send_message("Invalid channel selected.", ephemeral=True)
                    return
                deleted = await clear_channel_history(channel_id)
                await interaction.response.send_message(f"Cleared {deleted} messages from {target_channel.mention}.", ephemeral=True)
            elif target == "all":
                deleted = await clear_user_history()
                await interaction.response.send_message(f"Cleared {deleted} messages and comments from all channels.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages in that channel.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in clear command: {str(e)}")
            await interaction.response.send_message(f"An error occurred while clearing messages: {str(e)}", ephemeral=True)

    @clear_command.autocomplete("channel")
    async def clear_channel_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        return await get_channel_choices(interaction, current)
