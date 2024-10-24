import discord
from discord import app_commands
from src.utils.history.history_manager import show_history_page
from src.utils.history.channel_utils import get_channel_choices
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
        logger.info(f"Received /history command from user {interaction.user.id} with parameters: channel={channel}, page={page}, filter_type={filter_type}, user={user.id if user else None}")
        
        is_admin = interaction.user.guild_permissions.administrator
        logger.info(f"User {interaction.user.id} is admin: {is_admin}")

        if not is_admin and user and user != interaction.user:
            logger.warning(f"Non-admin user {interaction.user.id} attempted to view history for user {user.id}")
            await interaction.response.send_message("You don't have permission to view other users' history.", ephemeral=True)
            return

        # If no user is specified or the user is not an admin, set user to the interaction user
        if not user or not is_admin:
            user = interaction.user
            logger.info(f"Set user to interaction user: {user.id}")

        try:
            if channel:
                channel_id = int(channel)
                target_channel = interaction.guild.get_channel(channel_id)
                if target_channel is None:
                    logger.warning(f"Invalid channel ID provided: {channel_id}")
                    await interaction.response.send_message("Invalid channel selected.", ephemeral=True)
                    return
                logger.info(f"Selected channel: {channel_id}")
            else:
                channel_id = interaction.channel.id
                logger.info(f"Using current channel: {channel_id}")

            logger.info(f"Deferring response for history command (user: {user.id}, channel: {channel_id}, page: {page}, filter_type: {filter_type})")
            await interaction.response.defer(ephemeral=True)
            
            logger.info(f"Calling show_history_page for user {user.id}, channel {channel_id}, page {page}, filter_type {filter_type}")
            await show_history_page(interaction, channel_id, page, filter_type, user=user, ephemeral=True)
            
            logger.info(f"Successfully executed history command for user {user.id}, channel {channel_id}, page {page}, filter_type {filter_type}")
        except ValueError as ve:
            logger.error(f"ValueError in history command: {str(ve)}")
            await interaction.followup.send(f"Invalid input: {str(ve)}", ephemeral=True)
        except Exception as e:
            logger.error(f"Unexpected error in history command: {str(e)}", exc_info=True)
            await interaction.followup.send(f"An unexpected error occurred while retrieving history. Please try again later.", ephemeral=True)

    @history_command.autocomplete("channel")
    async def history_channel_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        logger.debug(f"Autocomplete request for channel with current input: {current}")
        choices = await get_channel_choices(interaction, current)
        logger.debug(f"Returned {len(choices)} channel choices for autocomplete")
        return choices
