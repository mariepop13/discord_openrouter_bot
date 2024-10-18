import discord
import asyncio
import logging
from src.utils.image_generation import generate_image
from src.commands.image_analysis import analyze_image_command as analyze_image_impl
from src.utils.models import GENERATE_IMAGE_MODELS

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def generate_image_command(interaction: discord.Interaction, prompt: str, model: str = "black-forest-labs/flux-dev", bot=None):
    if model not in GENERATE_IMAGE_MODELS:
        await interaction.followup.send(f"Invalid model. Please choose from: {', '.join(GENERATE_IMAGE_MODELS)}")
        return

    logger.debug(f"Received image generation request with prompt: {prompt}, model: {model}")
    await interaction.followup.send("Generating image... This may take a few minutes.")

    try:
        output = await generate_image(prompt, model)
        logger.debug(f"Output from generate_image: {output}")

        # Ensure we're using the actual model name in the message
        actual_model = model if model != "black-forest-labs/flux-dev" else "black-forest-labs/flux-dev"

        if isinstance(output, str) and output.startswith("http"):
            # This handles the flux-1.1-pro model and any other model that returns a direct URL
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            message = f"Generated image using model: {actual_model}\n{output}"
            await interaction.followup.send(content=message)
        elif isinstance(output, dict) and 'local_path' in output and 'url' in output:
            # This handles models that return a dictionary with local_path and url
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            message = f"Generated image using model: {actual_model}"
            file = discord.File(output['local_path'], filename='generated_image.webp')
            try:
                await interaction.followup.send(content=message, file=file)
            except discord.HTTPException as e:
                logger.error(f"Failed to send message: {str(e)}")
                await interaction.followup.send("The image was generated, but I couldn't send it due to a Discord error. Please try again.")
        else:
            logger.warning(f"Unexpected output format: {output}")
            await interaction.followup.send(f"Sorry, I couldn't generate the image. Unexpected output: {output}")
    except Exception as e:
        logger.error(f"Error occurred while generating image for prompt: {prompt}, Error: {str(e)}")
        await interaction.followup.send(f"Sorry, an error occurred while generating the image: {str(e)}. Please try again later.")

async def analyze_image_command(interaction: discord.Interaction, image: discord.Attachment):
    logger.debug(f"Received image analysis request for image: {image.filename}")
    await analyze_image_impl(interaction, image)
