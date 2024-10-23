import logging
import discord

async def handle_history_error(interaction: discord.Interaction, channel_id, error, ephemeral: bool = True):
    logging.error(f"Error in history command for channel {channel_id}: {str(error)}")
    error_message = "An error occurred while retrieving the chat history. Please try again later."
    await interaction.followup.send(error_message, ephemeral=ephemeral)
