import discord
import logging
from typing import List
from src.database.message_operations import get_messages_for_channel, get_messages_for_user
from src.utils.message_formatting import format_message
from src.config import MAX_EMBED_LENGTH, MESSAGES_PER_PAGE

async def get_channel_choices(interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
    choices = []
    for channel in interaction.guild.text_channels:
        if current.lower() in channel.name.lower():
            choices.append(discord.app_commands.Choice(name=channel.name, value=str(channel.id)))
    return choices[:25]  # Discord has a limit of 25 choices

async def show_history_page(interaction: discord.Interaction, channel_id: int, page: int = 1, filter_type: str = 'all', user: discord.User = None, ephemeral: bool = True):
    try:
        from src.views.history_pagination import HistoryPaginationView
        
        logging.debug(f"Fetching history for channel {channel_id}, page {page}, filter_type {filter_type}, user {user}")
        offset = (page - 1) * MESSAGES_PER_PAGE
        
        if user:
            chat_history = await get_messages_for_user(user.id, channel_id, MESSAGES_PER_PAGE, offset)
            total_messages = len(await get_messages_for_user(user.id, channel_id))
        else:
            chat_history = await get_messages_for_channel(channel_id, MESSAGES_PER_PAGE, offset)
            total_messages = len(await get_messages_for_channel(channel_id))
        
        if not chat_history:
            await send_no_history_message(interaction, page, user, ephemeral)
            return
        
        filtered_history = filter_history(chat_history, filter_type)
        formatted_history = format_history(filtered_history)
        chunks = create_chunks(formatted_history)
        
        total_pages = (total_messages + MESSAGES_PER_PAGE - 1) // MESSAGES_PER_PAGE

        embed = create_history_embed(interaction, page, total_pages, chunks, offset, total_messages, user)
        
        view = HistoryPaginationView(interaction.user.id, channel_id, page, total_pages, filter_type, show_history_page, user)
        view.update_buttons()

        await interaction.response.send_message(embed=embed, view=view, ephemeral=ephemeral)
        
        logging.debug(f"Successfully fetched and displayed history for channel {channel_id}, page {page}, user {user}")

    except Exception as e:
        await handle_history_error(interaction, channel_id, e, ephemeral)

async def send_no_history_message(interaction: discord.Interaction, page: int, user: discord.User = None, ephemeral: bool = True):
    if user:
        content = f"No chat history found for user {user.name} in this channel." if page == 1 else "No more history to display for this user."
    else:
        content = "This channel doesn't have any chat history yet." if page == 1 else "No more history to display."
    await interaction.response.send_message(content, ephemeral=ephemeral)
    logging.debug(f"No chat history found for channel {interaction.channel.id}, page {page}, user {user}")

def filter_history(chat_history, filter_type):
    return [
        message for message in chat_history
        if filter_type == 'all' or
        (filter_type == 'chat' and message[3] in ['user', 'bot']) or
        (filter_type == 'image' and message[3] == 'image_analysis')
    ]

def format_history(filtered_history):
    # Reverse the order of messages before formatting
    return "\n\n".join([format_message(*message) for message in reversed(filtered_history)])

def create_chunks(formatted_history):
    return [formatted_history[i:i+MAX_EMBED_LENGTH] for i in range(0, len(formatted_history), MAX_EMBED_LENGTH)]

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
    embed.set_footer(text=f"Showing messages {offset + 1}-{min(offset + MESSAGES_PER_PAGE, total_messages)} out of {total_messages}")
    return embed

async def handle_history_error(interaction: discord.Interaction, channel_id, error, ephemeral: bool = True):
    logging.error(f"Error in history command for channel {channel_id}: {str(error)}")
    error_message = "An error occurred while retrieving the chat history. Please try again later."
    await interaction.response.send_message(error_message, ephemeral=ephemeral)
