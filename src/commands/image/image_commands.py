import discord
import aiohttp
import os
from datetime import datetime
from src.utils.image.image_generation import generate_image
from src.commands.image.image_analysis import analyze_image_command as analyze_image_impl
from src.database.schema.models import GENERATE_IMAGE_MODELS
from src.utils.logging.logging_setup import setup_logger

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
        timestamp_filename = get_timestamp_filename()
        local_filename = f"generated_images/{timestamp_filename}"

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)

        output = await generate_image(prompt, model, local_filename)
        
        logger.debug(f"Output from generate_image: {output if isinstance(output, str) else {k: v for k, v in output.items() if k != 'url'}}")

        actual_model = model if model != "black-forest-labs/flux-dev" else "black-forest-labs/flux-dev"
        message = f"Generated image using model: {actual_model}"

        if isinstance(output, str) and output.startswith("http"):
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            if await download_image(output, local_filename):
                if os.path.exists(local_filename) and os.path.getsize(local_filename) > 0:
                    file = discord.File(local_filename, filename=timestamp_filename)
                    await interaction.followup.send(content=message, file=file)
                else:
                    await interaction.followup.send(f"{message}\nThe image was generated but the file is empty. You can view it here: {output}")
            else:
                await interaction.followup.send(f"{message}\nFailed to download the image, but you can view it here: {output}")
        elif isinstance(output, dict) and 'local_path' in output:
            logger.debug(f"Image generated successfully for prompt: {prompt}")
            if os.path.exists(output['local_path']) and os.path.getsize(output['local_path']) > 0:
                file = discord.File(output['local_path'], filename=timestamp_filename)
                try:
                    await interaction.followup.send(content=message, file=file)
                except discord.HTTPException as e:
                    logger.error(f"Failed to send message: {str(e)}")
                    await interaction.followup.send("The image was generated, but I couldn't send it due to a Discord error. Please try again.")
            else:
                await interaction.followup.send(f"{message}\nThe image was generated but the file is empty or missing.")
        else:
            logger.warning(f"Unexpected output format: {output}")
            await interaction.followup.send(f"Sorry, I couldn't generate the image. Unexpected output: {output}")
    except Exception as e:
        logger.error(f"Error occurred while generating image for prompt: {prompt}, Error: {str(e)}")
        await interaction.followup.send(f"Sorry, an error occurred while generating the image: {str(e)}. Please try again later.")

async def analyze_image_command(interaction: discord.Interaction, image: discord.Attachment):
    logger.debug(f"Received image analysis request for image: {image.filename}")
    await analyze_image_impl(interaction, image)
