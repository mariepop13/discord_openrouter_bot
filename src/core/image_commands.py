import discord
from discord import app_commands
from src.commands.image_commands import analyze_image_command, generate_image_command
from src.utils.models import GENERATE_IMAGE_MODELS
from src.utils.logging_setup import setup_logger

logger = setup_logger(__name__)

def register_image_commands(bot):
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
    @app_commands.describe(
        prompt="Your image generation prompt",
        model="The image generation model to use"
    )
    @app_commands.choices(model=[app_commands.Choice(name=model, value=model) for model in GENERATE_IMAGE_MODELS])
    async def generate_image(interaction: discord.Interaction, prompt: str, model: str = "black-forest-labs/flux-dev"):
        logger.debug(f"Received /generate_image command with prompt: {prompt}, model: {model}")
        await interaction.response.defer()
        await generate_image_command(interaction, prompt, model, bot)

    logger.info("Image commands registered successfully")
