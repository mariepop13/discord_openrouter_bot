import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.commands.ai_chat import ai_command
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def create_bot():
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix='!', intents=intents)

def initialize_bot():
    logger.info("Initializing bot...")
    bot = create_bot()

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
        
        client_id = os.getenv('CLIENT_ID')
        if client_id:
            permissions = discord.Permissions.text()
            invite_link = discord.utils.oauth_url(client_id, permissions=permissions, scopes=("bot", "applications.commands"))
            logger.info(f"Bot invite link: {invite_link}")
        else:
            logger.warning("CLIENT_ID not found in .env file. Invite link couldn't be generated.")

        try:
            synced = await bot.tree.sync()
            logger.info(f'Synced {len(synced)} commands globally.')
        except Exception as e:
            logger.error(f'Error syncing commands: {e}')

    @bot.event
    async def on_message(message):
        if bot.user.mentioned_in(message) and not message.mention_everyone and not message.content.startswith('/'):
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
            try:
                await ai_command(message, content)
            except Exception as e:
                logger.error(f"Error in ai_command: {e}")
                await message.channel.send("Sorry, I encountered an error while processing your request.")
        
        await bot.process_commands(message)

    return bot
