import discord
from discord import app_commands
from src.commands.ai_preferences import update_ai_settings
from src.commands.image_commands import analyze_image_command, generate_image_command, image_generation_help
from src.commands.general_commands import clear, ping, help_command
from src.commands.history_command import history
from src.commands.ai_chat import ai_command
from typing import Optional
from src.utils.models import MODELS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIOption(discord.Enum):
    personality = "personality"
    tone = "tone"
    language = "language"
    prebuild = "prebuild"
    max_tokens = "max_tokens"
    custom = "custom"

def register_commands(bot):
    # AI and Chat Commands
    @bot.tree.command(name="ai", description="Chat with the AI")
    @app_commands.describe(message="Your message to the AI")
    async def ai_command_wrapper(interaction: discord.Interaction, message: str):
        logger.debug(f"Received /ai command with message: {message}")
        await ai_command(interaction, message)

    @bot.tree.command(name="update_ai_settings", description="Update AI settings")
    @app_commands.describe(
        option="The AI option to set (optional)",
        value="The value to set for the chosen option (optional)",
        model="The AI model to use",
        custom_option="If 'custom' is selected, specify the custom option here"
    )
    @app_commands.choices(model=[app_commands.Choice(name=model, value=model) for model in MODELS])
    async def update_ai_settings_wrapper(
        interaction: discord.Interaction, 
        model: Optional[str] = None,
        option: Optional[AIOption] = None,
        value: Optional[str] = None,
        custom_option: Optional[str] = None
    ):
        option_value = custom_option if option == AIOption.custom else option.value if option else None
        logger.debug(f"Received /update_ai_settings command with model: {model}, option: {option}, value: {value}, custom_option: {custom_option}")
        await update_ai_settings(interaction, option_value, value, model)

    # Image Commands
    @bot.tree.command(name="analyze", description="Analyze an attached image")
    @app_commands.describe(image="The image to analyze")
    async def analyze(interaction: discord.Interaction, image: discord.Attachment):
        logger.debug(f"Received /analyze command with image: {image.filename}")
        if not image.content_type.startswith('image/'):
            await interaction.response.send_message("The uploaded file is not an image. Please upload an image file.")
            return
        await interaction.response.defer()
        await analyze_image_command(interaction, image)

    @bot.tree.command(name="generate_image", description="Generate an image based on a prompt")
    @app_commands.describe(prompt="Your image generation prompt")
    async def generate_image(interaction: discord.Interaction, prompt: str):
        logger.debug(f"Received /generate_image command with prompt: {prompt}")
        await interaction.response.defer()
        await generate_image_command(interaction, prompt, bot)

    @bot.tree.command(name="image_help", description="Get help with image generation commands")
    async def image_help_command(interaction: discord.Interaction):
        logger.debug("Received /image_help command")
        await interaction.response.defer()
        await image_generation_help(interaction)

    # Utility Commands
    @bot.tree.command(name="clear", description="Clear the database")
    async def clear_command(interaction: discord.Interaction):
        logger.debug("Received /clear command")
        await clear(interaction)

    @bot.tree.command(name="help", description="Get information about available commands")
    async def help_command_wrapper(interaction: discord.Interaction):
        logger.debug("Received /help command")
        await help_command(interaction)

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        logger.debug("Received /ping command")
        await ping(interaction)

    # Register the history command
    bot.tree.add_command(history)

    logger.info("All commands registered successfully.")
