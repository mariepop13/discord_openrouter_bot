import discord
import aiohttp
import os
from datetime import datetime
from src.utils.image_generation import generate_image
from src.commands.image_analysis import analyze_image_command as analyze_image_impl
from src.utils.models import GENERATE_IMAGE_MODELS
from src.utils.logging_setup import setup_logger

logger = setup_logger(__name__)

async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await resp.read())
                return True
    return False

def get_timestamp_filename():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S.webp")

async def generate_image_command(interaction: discord.Interaction, prompt: str, model: str = "black-forest-labs/flux-dev", bot=None):
    if model not in GENERATE_IMAGE_MODELS:
        await interaction.followup.send(f"Invalid model. Please choose from: {', '.join(GENERATE_IMAGE_MODELS)}")
        return

    logger.debug(f"Received image generation request with prompt: {prompt}, model: {model}")
    await interaction.followup.send("Generating image... This may take a few minutes.")

    try:
        output = await generate_image(prompt, model)
        logger.debug(f"Output from generate_image: {output}")

        actual_model = model if model != "black-forest-labs/flux-dev" else "black-forest-labs/flux-dev"
        timestamp_filename = get_timestamp_filename()
        local_filename = f"generated_images/{timestamp_filename}"

        if isinstance(output, str) and output.startswith("http"):
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            message = f"Generated image using model: {actual_model}"
            
            if await download_image(output, local_filename):
                file = discord.File(local_filename, filename=timestamp_filename)
                await interaction.followup.send(content=message, file=file)
            else:
                await interaction.followup.send(f"{message}\nFailed to download the image, but you can view it here: {output}")
        elif isinstance(output, dict) and 'local_path' in output and 'url' in output:
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            message = f"Generated image using model: {actual_model}"
            os.rename(output['local_path'], local_filename)
            file = discord.File(local_filename, filename=timestamp_filename)
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
