import discord
from utils.api_utils import analyze_image
import logging

async def analyze_image_command(ctx, image: discord.Attachment):
    try:
        image_url = image.url
        description = await analyze_image(image_url)
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(f"Image analysis: {description}")
        else:
            await ctx.send(f"Image analysis: {description}")
    except Exception as e:
        error_message = f"Sorry, I couldn't analyze the image. Error: {str(e)}"
        logging.error(f"Error in analyze_image_command: {str(e)}")
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(error_message)
        else:
            await ctx.send(error_message)
