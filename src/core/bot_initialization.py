import os
import discord
from discord import Permissions
from discord.ext import commands
from dotenv import load_dotenv
from src.commands.ai_chat import ai_command
from src.utils.logging_utils import get_logger
from src.utils.log_cleanup import cleanup_logs
from src.database.database_schema import setup_database
import asyncio

logger = get_logger(__name__)

def create_bot():
    logger.debug("Creating bot with default intents...")
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot_name = os.getenv('BOT_NAME', 'Discord Image Analysis Bot')
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.bot_name = bot_name  # Store the bot name as an attribute
    logger.debug(f"Bot '{bot_name}' created successfully.")
    return bot

def initialize_bot():
    logger.debug("Initializing bot...")
    
    # Clean up log files before initializing the bot
    log_files_to_keep = int(os.getenv('LOG_FILES_TO_KEEP', 5))
    logger.info(f"Cleaning up log files, keeping the {log_files_to_keep} most recent files.")
    cleanup_logs(keep_latest=log_files_to_keep)  # Pass the value to cleanup_logs
    logger.info("Log cleanup completed.")
    
    bot = create_bot()

    @bot.event
    async def on_ready():
        logger.info(f"Bot '{bot.bot_name}' is ready.")
        logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
        
        # Set up the database
        logger.info("Setting up the database...")
        await setup_database()
        logger.info("Database setup completed.")
        
        # Set the bot's status to online with a custom activity
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Ready to chat!"))
        logger.info("Bot status set to online with 'Ready to chat!' activity.")
        
        client_id = os.getenv('CLIENT_ID')
        if client_id:
            # Create permissions that include text permissions and the ability to delete messages
            permissions = Permissions(
            send_messages=True,        # Send messages (for general commands like /help, /ping)
            read_messages=True,        # Read messages (to respond to commands and read channels)
            manage_messages=True,      # Manage messages (for commands like /clear)
            view_channel=True,         # View channels (to access multiple channels)
            read_message_history=True  # Read message history (for /history command)
            )
            invite_link = discord.utils.oauth_url(client_id, permissions=permissions, scopes=("bot", "applications.commands"))
            logger.info(f"Bot invite link: {invite_link}")
        else:
            logger.warning("CLIENT_ID not found in .env file. Invite link couldn't be generated.")

        await force_sync(bot)

    @bot.event
    async def on_message(message):
        logger.debug(f"Received message: {message.content} from {message.author}")
        if bot.user.mentioned_in(message) and not message.mention_everyone and not message.content.startswith('/'):
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
            logger.debug(f"Bot was mentioned. Processing message: {content}")
            try:
                await ai_command(message, content)
                logger.debug("ai_command executed successfully.")
            except Exception as e:
                logger.error(f"Error in ai_command: {e}")
                await message.channel.send(f"Sorry, I ({bot.bot_name}) encountered an error while processing your request.")
        
        await bot.process_commands(message)
        logger.debug("Processed commands for the message.")

    # Add the forcesync command to the bot
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

    return bot

async def force_sync(bot):
    logger.info("Forcing a re-sync of all commands...")
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} commands globally.')
        return synced
    except Exception as e:
        logger.error(f'Error syncing commands: {e}')
        return None
