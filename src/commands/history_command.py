import discord
from discord import app_commands
from src.utils.history_utils import show_history_page, get_channel_choices
from typing import Optional, Literal, List
import logging

logger = logging.getLogger(__name__)

def register_history_command(bot):
    @bot.tree.command(name="history", description="View your chat history or specify a user (admin only) for the current or specified channel")
    @app_commands.describe(
        channel="The channel to view history for (optional)",
        page="The page number to view (default: 1)",
        filter_type="Filter type: 'all', 'chat', or 'image' (default: all)",
        user="The user to view history for (admin only, optional)"
    )
    async def history_command(
        interaction: discord.Interaction,
        channel: Optional[str] = None,
        page: int = 1,
        filter_type: Literal["all", "chat", "image"] = "all",
        user: Optional[discord.User] = None
    ):
        logger.debug(f"Received /history command with channel: {channel}, page: {page}, filter_type: {filter_type}, user: {user}")
        
        is_admin = interaction.user.guild_permissions.administrator

        if not is_admin and user and user != interaction.user:
            await interaction.response.send_message("You don't have permission to view other users' history.", ephemeral=True)
            return

        # If no user is specified or the user is not an admin, set user to the interaction user
        if not user or not is_admin:
            user = interaction.user

        try:
            if channel:
                channel_id = int(channel)
                target_channel = interaction.guild.get_channel(channel_id)
                if target_channel is None:
                    await interaction.response.send_message("Invalid channel selected.", ephemeral=True)
                    return
            else:
                channel_id = interaction.channel.id

            await interaction.response.defer(ephemeral=True)
            await show_history_page(interaction, channel_id, page, filter_type, user=user, ephemeral=True)
        except Exception as e:
            logger.error(f"Error in history command: {str(e)}")
            await interaction.followup.send(f"An error occurred while retrieving history: {str(e)}", ephemeral=True)

    @history_command.autocomplete("channel")
    async def history_channel_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        return await get_channel_choices(interaction, current)
