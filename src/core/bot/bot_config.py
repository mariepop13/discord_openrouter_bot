import os
import discord
from discord import Permissions
from discord.ext import commands
from dotenv import load_dotenv
from src.utils.logging.logging_utils import get_logger

logger = get_logger(__name__)

def create_bot():
    """Create and configure the Discord bot with default intents."""
    logger.debug("Creating bot with default intents...")
    load_dotenv()
    
    intents = discord.Intents.default()
    intents.message_content = True
    bot_name = os.getenv('BOT_NAME', 'Discord Image Analysis Bot')
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.bot_name = bot_name
    
    logger.debug(f"Bot '{bot_name}' created successfully.")
    return bot

def generate_invite_link(bot):
    """Generate and log the bot's invite link."""
    client_id = os.getenv('CLIENT_ID')
    if not client_id:
        logger.warning("CLIENT_ID not found in .env file. Invite link couldn't be generated.")
        return None
        
    permissions = Permissions(
        send_messages=True,
        read_messages=True,
        manage_messages=True,
        view_channel=True,
        read_message_history=True
    )
    invite_link = discord.utils.oauth_url(
        client_id, 
        permissions=permissions, 
        scopes=("bot", "applications.commands")
    )
    logger.info(f"Bot invite link: {invite_link}")
    return invite_link
