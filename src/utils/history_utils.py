import discord
import logging
from typing import List
from src.database.history_retrieval import get_history
from src.utils.message_formatting import format_message
from config import MAX_EMBED_LENGTH, MESSAGES_PER_PAGE

async def get_channel_choices(interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
    choices = []
    for channel in interaction.guild.text_channels:
        if current.lower() in channel.name.lower():
            choices.append(discord.app_commands.Choice(name=channel.name, value=str(channel.id)))
    return choices[:25]  # Discord has a limit of 25 choices

async def show_history_page(interaction: discord.Interaction, channel_id: int, page: int = 1, filter_type: str = 'all', user: discord.User = None, ephemeral: bool = True):
    try:
        from src.views.history_pagination import HistoryPaginationView
        
        logging.info(f"Fetching history for channel {channel_id}, page {page}, filter_type {filter_type}, user {user}")
        
        user_id = user.id if user else interaction.user.id
        total_messages = await get_history(user_id, channel_id, count_only=True)
        
        logging.info(f"Total messages in database for user {user_id}, channel {channel_id}: {total_messages}")
        
        # Calculate the correct offset for reversed order
        total_pages = (total_messages + MESSAGES_PER_PAGE - 1) // MESSAGES_PER_PAGE
        offset = max(0, total_messages - page * MESSAGES_PER_PAGE)
        
        chat_history = await get_history(user_id, channel_id, MESSAGES_PER_PAGE, offset)
        
        logging.info(f"Retrieved {len(chat_history)} messages from database for display")
        
        if not chat_history:
            await send_no_history_message(interaction, page, user, ephemeral)
            return
        
        # Reverse the order of messages to display newest first
        chat_history.reverse()
        
        filtered_history = filter_history(chat_history, filter_type)
        
        bot_message_count = sum(1 for message in filtered_history if message[3] == 'bot')
        logging.info(f"Number of bot messages in filtered history: {bot_message_count}")
        
        # Log detailed information about each message
        for idx, message in enumerate(filtered_history, 1):
            logging.info(f"Message {idx}: Type: {message[3]}, Content: {message[1][:50]}...")
        
        formatted_history = format_history(filtered_history)
        chunks = create_chunks(formatted_history)
        
        embed = create_history_embed(interaction, page, total_pages, chunks, offset, total_messages, user)
        
        view = HistoryPaginationView(interaction.user.id, channel_id, page, total_pages, filter_type, show_history_page, user)
        view.update_buttons()

        await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
        
        logging.info(f"Successfully fetched and displayed history for channel {channel_id}, page {page}, user {user}")

    except Exception as e:
        await handle_history_error(interaction, channel_id, e, ephemeral)

async def send_no_history_message(interaction: discord.Interaction, page: int, user: discord.User = None, ephemeral: bool = True):
    if user:
        content = f"No chat history found for user {user.name} in this channel." if page == 1 else "No more history to display for this user."
    else:
        content = "This channel doesn't have any chat history yet." if page == 1 else "No more history to display."
    await interaction.followup.send(content, ephemeral=ephemeral)
    logging.info(f"No chat history found for channel {interaction.channel.id}, page {page}, user {user}")

def filter_history(chat_history, filter_type):
    filtered = [
        message for message in chat_history
        if filter_type == 'all' or
        (filter_type == 'chat' and message[3] in ['user', 'bot']) or
        (filter_type == 'image' and message[3] == 'image_analysis')
    ]
    logging.info(f"Filtered history contains {len(filtered)} messages. Filter type: {filter_type}")
    return filtered

def format_history(filtered_history):
    formatted = "\n\n".join([
        format_message(
            message[0],  # user_id
            message[1],  # content
            message[2],  # model
            message[3],  # message_type
            message[4],  # timestamp
            message[5] if len(message) > 5 else None  # mentioned_user_id (if present)
        ) for message in filtered_history
    ])
    logging.info(f"Formatted {len(filtered_history)} messages for display")
    return formatted

def create_chunks(formatted_history):
    chunks = [formatted_history[i:i+MAX_EMBED_LENGTH] for i in range(0, len(formatted_history), MAX_EMBED_LENGTH)]
    logging.info(f"Created {len(chunks)} chunks for display")
    return chunks

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

async def handle_history_error(interaction: discord.Interaction, channel_id, error, ephemeral: bool = True):
    logging.error(f"Error in history command for channel {channel_id}: {str(error)}")
    error_message = "An error occurred while retrieving the chat history. Please try again later."
    await interaction.followup.send(error_message, ephemeral=ephemeral)
