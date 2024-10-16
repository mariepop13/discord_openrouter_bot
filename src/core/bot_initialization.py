import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.commands.ai_chat import ai_command
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def create_bot():
    logger.debug("Creating bot with default intents...")
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    logger.debug("Bot created successfully.")
    return bot

def initialize_bot():
    logger.debug("Initializing bot...")
    bot = create_bot()

    @bot.event
    async def on_ready():
        logger.info("Bot is ready.")
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
        logger.debug(f"Received message: {message.content} from {message.author}")
        if bot.user.mentioned_in(message) and not message.mention_everyone and not message.content.startswith('/'):
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
            logger.debug(f"Bot was mentioned. Processing message: {content}")
            try:
                await ai_command(message, content)
                logger.debug("ai_command executed successfully.")
            except Exception as e:
                logger.error(f"Error in ai_command: {e}")
                await message.channel.send("Sorry, I encountered an error while processing your request.")
        
        await bot.process_commands(message)
        logger.debug("Processed commands for the message.")

    return bot
