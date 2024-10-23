import discord
import logging
from config import MESSAGES_PER_PAGE

def create_history_embed(interaction: discord.Interaction, page, total_pages, chunks, offset, total_messages, user: discord.User = None):
    title = f"Chat History for #{interaction.channel.name}"
    if user:
        title += f" - User: {user.name}"
    title += f" (Page {page}/{total_pages})"
    
    embed = discord.Embed(
        title=title,
        description=chunks[0] if chunks else "No messages to display for this filter.",
        color=discord.Color.blue()
    )
    
    # Update the footer to correctly reflect the message range being displayed
    start_message = max(1, total_messages - offset)
    end_message = min(total_messages, start_message + MESSAGES_PER_PAGE - 1)
    embed.set_footer(text=f"Showing messages {end_message}-{start_message} out of {total_messages}")
    
    logging.info(f"Created embed for page {page}/{total_pages}, showing messages {end_message}-{start_message} out of {total_messages}")
    return embed
