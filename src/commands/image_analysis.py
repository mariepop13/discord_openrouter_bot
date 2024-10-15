import discord
from src.utils.api_utils import analyze_image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def analyze_image_command(ctx, image: discord.Attachment):
    try:
        logger.info("Received image for analysis: %s", image.filename)
        image_url = image.url
        description = await analyze_image(image_url)
        logger.info("Image analysis completed: %s", description)
        
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(f"Image analysis: {description}")
        else:
            await ctx.send(f"Image analysis: {description}")
    except Exception as e:
        error_message = f"Sorry, I couldn't analyze the image. Error: {str(e)}"
        logger.error("Error in analyze_image_command: %s", str(e))
        
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(error_message)
        else:
            await ctx.send(error_message)
