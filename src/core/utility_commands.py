import discord
from src.commands.general_commands import ping, help_command
import logging

logger = logging.getLogger(__name__)

def register_utility_commands(bot):
    @bot.tree.command(name="help", description="Get information about available commands")
    async def help_command_wrapper(interaction: discord.Interaction):
        logger.debug("Received /help command")
        await help_command(interaction)

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        logger.debug("Received /ping command")
        await ping(interaction)