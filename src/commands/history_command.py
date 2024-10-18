import discord
from discord import app_commands
from src.utils.history_utils import show_history_page, get_channel_choices
from typing import Optional, Literal, List
import logging

logger = logging.getLogger(__name__)

def register_history_command(bot):
    @bot.tree.command(name="history", description="View chat history for the current or specified channel")
    @app_commands.describe(
        channel="The channel to view history for (optional)",
        page="The page number to view (default: 1)",
        filter_type="Filter type: 'all', 'chat', or 'image' (default: all)"
    )
    async def history_command(
        interaction: discord.Interaction,
        channel: Optional[str] = None,
        page: int = 1,
        filter_type: Literal["all", "chat", "image"] = "all"
    ):
        logger.debug(f"Received /history command with channel: {channel}, page: {page}, filter_type: {filter_type}")
        
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have permission to view history.", ephemeral=True)
            return

        try:
            if channel:
                channel_id = int(channel)
                target_channel = interaction.guild.get_channel(channel_id)
                if target_channel is None:
                    await interaction.response.send_message("Invalid channel selected.", ephemeral=True)
                    return
            else:
                channel_id = interaction.channel.id

            await show_history_page(interaction, channel_id, page, filter_type, ephemeral=True)
        except Exception as e:
            logger.error(f"Error in history command: {str(e)}")
            await interaction.response.send_message(f"An error occurred while retrieving history: {str(e)}", ephemeral=True)

    @history_command.autocomplete("channel")
    async def history_channel_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        return await get_channel_choices(interaction, current)
