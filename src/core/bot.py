import os
import logging
from dotenv import load_dotenv
from src.core.bot_initialization import initialize_bot
from src.commands.ai_chat import ai_command
from src.commands.history_command import history
from src.commands.image_commands import generate_image, analyze_image
from src.utils.models import MODELS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded.")

# Initialize the bot
bot = initialize_bot()
logger.info("Bot initialized.")

@bot.tree.command(name="models", description="List available AI models")
async def list_models(interaction):
    model_list = "\n".join([f"- {model.split('/')[-1]}" for model in MODELS])
    await interaction.response.send_message(f"Available models:\n{model_list}")
    logger.info("Listed available models.")

# Add commands to the bot
bot.tree.add_command(ai_command)
logger.info("Added AI command.")
bot.tree.add_command(history)
logger.info("Added history command.")
bot.tree.add_command(generate_image)
logger.info("Added generate image command.")
bot.tree.add_command(analyze_image)
logger.info("Added analyze image command.")

# Run the bot
if __name__ == "__main__":
    logger.info("Starting the bot.")
    bot.run(os.getenv('DISCORD_TOKEN'))
    logger.info("Bot is running.")
    