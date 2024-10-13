import os
from dotenv import load_dotenv
from src.core.bot_initialization import initialize_bot
from src.commands.ai_chat import ai_command
from src.commands.history_command import history
from src.commands.image_commands import generate_image, analyze_image
from src.utils.models import MODELS

# Load environment variables
load_dotenv()

# Initialize the bot
bot = initialize_bot()

@bot.tree.command(name="models", description="List available AI models")
async def list_models(interaction):
    model_list = "\n".join([f"- {model.split('/')[-1]}" for model in MODELS])
    await interaction.response.send_message(f"Available models:\n{model_list}")

# Add commands to the bot
bot.tree.add_command(ai_command)
bot.tree.add_command(history)
bot.tree.add_command(generate_image)
bot.tree.add_command(analyze_image)

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))
