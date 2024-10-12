import os
from dotenv import load_dotenv
from core.bot_initialization import initialize_bot
from commands.ai_chat import ai_command
from commands.history_command import history
from commands.image_commands import generate_image, analyze_image

# Load environment variables
load_dotenv()

# Initialize the bot
bot = initialize_bot()

# Available models (consider moving this to a config file)
MODELS = [
    "google/gemini-flash-1.5",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4",
    "anthropic/claude-2",
    "google/palm-2-chat-bison",
    "meta-llama/llama-2-70b-chat"
]

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
