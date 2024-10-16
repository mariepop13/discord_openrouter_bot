import os
import logging
from dotenv import load_dotenv
from src.core.bot_initialization import initialize_bot
from src.core.command_registration import register_commands
from src.utils.models import MODELS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded.")

# Initialize the bot
bot = initialize_bot()
logger.debug("Bot initialized.")

# Register commands
register_commands(bot)
logger.debug("Commands registered.")

@bot.tree.command(name="models", description="List available AI models")
async def list_models(interaction):
    model_list = "\n".join([f"- {model.split('/')[-1]}" for model in MODELS])
    await interaction.response.send_message(f"Available models:\n{model_list}")
    logger.debug("Listed available models.")

# Run the bot
if __name__ == "__main__":
    logger.debug("Starting the bot.")
    bot.run(os.getenv('DISCORD_TOKEN'))
    logger.debug("Bot is running.")
