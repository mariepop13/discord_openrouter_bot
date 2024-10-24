import discord
import logging
from typing import List
from src.database.operations.history_retrieval import get_history
from config import MESSAGES_PER_PAGE

# Import all components
from .channel_utils import get_channel_choices
from .message_filter import filter_history
from .display import format_history, create_chunks, send_no_history_message
from .embed_creator import create_history_embed
from .error_handler import handle_history_error

# Lazy import to avoid circular dependency
def get_pagination_view():
    from src.views.history_pagination import HistoryPaginationView
    return HistoryPaginationView

async def show_history_page(interaction: discord.Interaction, channel_id: int, page: int = 1, filter_type: str = 'all', user: discord.User = None, ephemeral: bool = True):
    try:
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
        
        HistoryPaginationView = get_pagination_view()
        view = HistoryPaginationView(interaction.user.id, channel_id, page, total_pages, filter_type, show_history_page, user)
        view.update_buttons()

        await interaction.followup.send(embed=embed, view=view, ephemeral=ephemeral)
        
        logging.info(f"Successfully fetched and displayed history for channel {channel_id}, page {page}, user {user}")

    except Exception as e:
        logging.error(f"Error in show_history_page: {str(e)}", exc_info=True)
        await handle_history_error(interaction, channel_id, e, ephemeral)
