import discord
from src.utils.api_utils import analyze_image
from src.database.database_operations import get_history, insert_message
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
HISTORY_LIMIT = 20

def format_chat_history(history):
    formatted_history = []
    for _, content, _, message_type, _ in history:
        role = "user" if message_type == "user" else "assistant"
        formatted_history.append({"role": role, "content": content})
    logger.debug(f"Formatted chat history: {formatted_history}")
    return formatted_history

async def analyze_image_command(ctx, image: discord.Attachment):
    try:
        logger.info("Received image for analysis: %s", image.filename)
        image_url = image.url

        user_id = ctx.author.id if hasattr(ctx, 'author') else ctx.user.id

        # Retrieve chat history from the database
        db_history = await get_history(user_id, HISTORY_LIMIT)
        formatted_history = format_chat_history(db_history)

        # Add the current image analysis request to the history
        current_message = {"role": "user", "content": f"Analyze this image: {image_url}"}
        formatted_history.append(current_message)

        description = await analyze_image(image_url, formatted_history)
        logger.info("Image analysis completed: %s", description)
        
        # Insert the user's request and bot's response into the database
        await insert_message(user_id, f"Analyze this image: {image_url}", "image_analysis", 'user')
        await insert_message(CLIENT_ID, description, "image_analysis", 'bot')

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
