import discord
from discord import app_commands
import logging
from src.utils.history_utils import show_history_page

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app_commands.command(name="history", description="View chat history for the current or specified channel")
@app_commands.choices(filter_type=[
    app_commands.Choice(name="All", value="all"),
    app_commands.Choice(name="Chat only", value="chat"),
    app_commands.Choice(name="Image analyses only", value="image")
])
async def history(interaction: discord.Interaction, channel: discord.TextChannel = None, page: int = 1, filter_type: str = "all"):
    logging.debug(f"History command invoked by user {interaction.user.id}, channel {channel.id if channel else interaction.channel.id}, page {page}, filter_type {filter_type}")
    await interaction.response.defer(ephemeral=True)
    channel_id = channel.id if channel else interaction.channel.id
    await show_history_page(interaction, channel_id, page, filter_type)

async def setup(bot):
    bot.tree.add_command(history)
    logging.debug("History command added to bot")
