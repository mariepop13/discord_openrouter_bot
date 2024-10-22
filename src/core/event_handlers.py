import discord
from src.commands.ai_chat import ai_command
from src.utils.logging_utils import get_logger
from .database_init import initialize_database
from .sync_commands import force_sync

logger = get_logger(__name__)

def setup_event_handlers(bot):
    """Set up event handlers for the bot."""
    
    @bot.event
    async def on_ready():
        logger.info(f"Bot '{bot.bot_name}' is ready.")
        logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
        
        await initialize_database()
        
        # Set the bot's status
        await bot.change_presence(
            status=discord.Status.online, 
            activity=discord.Game(name="Ready to chat!")
        )
        logger.info("Bot status set to online with 'Ready to chat!' activity.")

        await force_sync(bot)

    @bot.event
    async def on_message(message):
        logger.debug(f"Received message: {message.content} from {message.author}")
        
        if (bot.user.mentioned_in(message) and 
            not message.mention_everyone and 
            not message.content.startswith('/')):
            
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
            logger.debug(f"Bot was mentioned. Processing message: {content}")
            
            try:
                await ai_command(message, content)
                logger.debug("ai_command executed successfully.")
            except Exception as e:
                logger.error(f"Error in ai_command: {e}")
                await message.channel.send(
                    f"Sorry, I ({bot.bot_name}) encountered an error while processing your request."
                )
        
        await bot.process_commands(message)
        logger.debug("Processed commands for the message.")
