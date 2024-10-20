import discord
from discord import Interaction
from discord.ext import commands
from src.database.database_operations import clear_user_history
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_message(interaction: Interaction, content: str, ephemeral: bool = True, embed: Optional[discord.Embed] = None):
    try:
        if embed:
            await interaction.response.send_message(content=content, embed=embed, ephemeral=ephemeral)
        else:
            await interaction.response.send_message(content, ephemeral=ephemeral)
        logger.debug(f"Message sent: {content}")
    except discord.errors.NotFound:
        if embed:
            await interaction.followup.send(content=content, embed=embed, ephemeral=ephemeral)
        else:
            await interaction.followup.send(content, ephemeral=ephemeral)
        logger.debug(f"Follow-up message sent: {content}")

async def ping(interaction: Interaction):
    logger.debug("Ping command received")
    await send_message(interaction, 'Pong!', ephemeral=False)

async def help_command(interaction: Interaction):
    logger.debug("Help command received")
    help_embed = discord.Embed(title="Discord OpenRouter Bot", color=discord.Color.blue())
    
    help_embed.description = ("This bot uses OpenRouter.ai API to interact with various AI models, "
                              "analyze images, and generate images using Replicate. "
                              "The bot responds when mentioned and uses the following commands:")

    commands = {
        "General Commands": [
            ("/help", "Show this help message"),
            ("/ping", "Check if the bot is responsive"),
            ("/clear", "Clear all conversation history"),
            ("/purge [amount]", "Delete a specified number of messages (or all if no amount is given)")
        ],
        "AI Commands": [
            ("/ai [message]", "Chat with the AI"),
            ("/analyze [image]", "Analyze an attached image"),
            ("/update_ai_settings", "Update AI settings (model, personality, tone, language, max tokens)")
        ],
        "Image Commands": [
            ("/generate_image [prompt]", "Generate an image based on a prompt"),
            ("/image_help", "Get help with image generation commands")
        ]
    }
    
    for category, command_list in commands.items():
        help_embed.add_field(
            name=category, 
            value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in command_list]), 
            inline=False
        )
    
    help_embed.add_field(
        name="Usage Examples",
        value=("• Chat with AI: `/ai Hello, how are you?`\n"
               "• Analyze an image: `/analyze` (attach an image to your message)\n"
               "• Generate an image: `/generate_image A beautiful sunset over the ocean`\n"
               "• Update AI settings: `/update_ai_settings model:openai/gpt-4o option:max_tokens value:2000`\n"
               "• Purge messages: `/purge 10` (deletes last 10 messages)"),
        inline=False
    )
    
    await send_message(interaction, content="", embed=help_embed, ephemeral=False)
    logger.debug("Help message sent")

async def clear(interaction: Interaction):
    logger.debug("Clear command received")
    try:
        rows_deleted = await clear_user_history()
        response_message = f"All conversation history has been cleared. {rows_deleted} entries have been deleted."
        await send_message(interaction, response_message)
        logger.debug(f"Clear command successful: {rows_deleted} entries deleted")
    except Exception as e:
        logging.error(f"Error in clear command: {str(e)}")
        await send_message(interaction, "An error occurred while clearing the conversation history. Please try again later.")
        logger.error("Clear command failed")

async def purge(interaction: Interaction, amount: int = None):
    logger.debug(f"Purge command received with amount: {amount}")
    try:
        await interaction.response.defer(ephemeral=True)
        
        if amount is None:
            deleted = await interaction.channel.purge(limit=None)
            logger.info(f"All messages purged from the channel")
        else:
            deleted = await interaction.channel.purge(limit=amount)
            logger.info(f"{len(deleted)} messages purged from the channel")
        
        await interaction.followup.send(f"{len(deleted)} message(s) have been deleted.", ephemeral=True)
    except discord.errors.Forbidden:
        await interaction.followup.send("I don't have the required permissions to delete messages. Please make sure I have the 'Manage Messages' permission in this channel.", ephemeral=True)
        logger.error("Purge command failed due to insufficient permissions")
    except Exception as e:
        await interaction.followup.send("An error occurred while trying to delete messages.", ephemeral=True)
        logger.error(f"Error in purge command: {str(e)}")
