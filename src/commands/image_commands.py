import discord
import asyncio
import logging
from src.utils.api_utils import generate_image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_image_command(interaction: discord.Interaction, prompt: str, bot):
    logger.debug(f"Received image generation request with prompt: {prompt}")
    await interaction.followup.send("Generating image... This may take a few minutes.")

    try:
        output = await generate_image(prompt)
        if output:
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            await interaction.followup.send(f"Generated image: {output}")
        else:
            logger.warning(f"Image generation failed for prompt: {prompt}")
            await interaction.followup.send("Sorry, I couldn't generate the image. Please try again with a different prompt.")
    except Exception as e:
        logger.error(f"Error occurred while generating image for prompt: {prompt}, Error: {str(e)}")
        await interaction.followup.send(f"Sorry, an error occurred while generating the image: {str(e)}")

async def image_generation_help(interaction: discord.Interaction):
    help_text = """
    Image Generation Command Help:
    
    Usage: /generate_image <prompt>
    
    Options:
    - prompt: Your description of the image you want to generate.
    
    Example:
    /generate_image A beautiful sunset over the ocean
    
    Note: Image generation may take a few minutes. Please be patient.
    """
    logger.debug("Sending image generation help text.")
    await interaction.followup.send(help_text)

async def analyze_image_command(interaction: discord.Interaction, image: discord.Attachment):
    logger.debug(f"Received image analysis request for image: {image.filename}")
    from src.commands.image_analysis import analyze_image_command as analyze_image_impl
    await analyze_image_impl(interaction, image)
