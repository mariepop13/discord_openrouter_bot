import discord
from discord import Interaction
from utils.database_operations import clear_user_history
import logging
from typing import Optional

async def send_message(interaction: Interaction, content: str, ephemeral: bool = True, embed: Optional[discord.Embed] = None):
    try:
        if embed:
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.response.send_message(content, ephemeral=ephemeral)
    except discord.errors.NotFound:
        if embed:
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)
        else:
            await interaction.followup.send(content, ephemeral=ephemeral)

async def ping(interaction: Interaction):
    await send_message(interaction, 'Pong!', ephemeral=False)

async def help_command(interaction: Interaction):
    help_embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    
    commands = {
        "General Commands": [
            ("/help", "Show this help message"),
            ("/ping", "Check if the bot is responsive"),
            ("/clear", "Clear all conversation history"),
            ("/sync", "Synchronize slash commands (Admin only)")
        ],
        "AI Commands": [
            ("/ai [message]", "Chat with the AI"),
            ("/analyze [image]", "Analyze an attached image")
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
    
    await send_message(interaction, embed=help_embed, ephemeral=False)

async def clear(interaction: Interaction):
    try:
        rows_deleted = await clear_user_history()
        response_message = f"All conversation history has been cleared. {rows_deleted} entries have been deleted."
        await send_message(interaction, response_message)
    except Exception as e:
        logging.error(f"Error in clear command: {str(e)}")
        await send_message(interaction, "An error occurred while clearing the conversation history. Please try again later.")
