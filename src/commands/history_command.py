import discord
from discord.ext import commands
import logging
from src.utils.history_utils import show_history_page

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HistoryCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="history", description="View chat history for the current or specified channel")
    @commands.has_permissions(administrator=True)
    async def history(self, ctx, channel: discord.TextChannel = None, page: int = 1, filter_type: str = "all"):
        logging.debug(f"History command invoked by user {ctx.author.id}, channel {channel.id if channel else ctx.channel.id}, page {page}, filter_type {filter_type}")
        
        channel_id = channel.id if channel else ctx.channel.id
        
        await show_history_page(ctx, channel_id, page, filter_type)

async def setup(bot):
    await bot.add_cog(HistoryCommand(bot))
    logging.debug("History command added to bot")
