from discord.ext import commands
from src.utils.logging.logging_utils import get_logger

logger = get_logger(__name__)

async def force_sync(bot):
    """Force a re-sync of all commands."""
    logger.info("Forcing a re-sync of all commands...")
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} commands globally.')
        return synced
    except Exception as e:
        logger.error(f'Error syncing commands: {e}')
        return None

def setup_sync_command(bot):
    """Add the forcesync command to the bot."""
    @commands.is_owner()
    @commands.command(name='forcesync', hidden=True)
    async def forcesync(ctx):
        logger.info(f"Force sync requested by {ctx.author}")
        synced = await force_sync(ctx.bot)
        if synced:
            await ctx.send(f'Synced {len(synced)} commands globally.')
        else:
            await ctx.send('Failed to sync commands. Check logs for details.')

    bot.add_command(forcesync)
    logger.info("Added forcesync command to the bot.")
