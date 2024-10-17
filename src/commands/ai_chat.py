import discord
from src.utils.api_utils import chat_with_ai
from src.database.database_operations import get_personalization, get_ai_preferences
from src.database.message_operations import insert_message, get_messages_for_channel
import logging
import os
from collections import defaultdict
import time
from typing import Union, Optional

CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
COOLDOWN_TIME = 5
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT'))

last_response_time = defaultdict(float)

def is_on_cooldown(user_id: int) -> bool:
    on_cooldown = time.time() - last_response_time[user_id] < COOLDOWN_TIME
    logging.debug(f"User {user_id} is {'on' if on_cooldown else 'not on'} cooldown.")
    return on_cooldown

def update_cooldown(user_id: int) -> None:
    last_response_time[user_id] = time.time()
    logging.debug(f"Updated cooldown for user {user_id}.")

def get_personalized_message(personalization: tuple, message: str) -> str:
    if not personalization:
        logging.debug("No personalization found.")
        return message

    pers, tn, lang, _, _ = personalization
    parts = [f"a {pers} personality" if pers else None,
             f"a {tn} tone" if tn else None,
             f"in {lang} language" if lang else None]
    parts = [p for p in parts if p]
    
    if parts:
        personalized_message = f"Please respond with {', '.join(parts)}. User message: {message}"
        logging.debug(f"Personalized message: {personalized_message}")
        return personalized_message
    return message

def format_chat_history(history):
    formatted_history = []
    for user_id, content, model, message_type, timestamp in history:
        if message_type == "user":
            role = "user"
        elif message_type == "bot":
            role = "assistant"
        elif message_type == "image_analysis":
            role = "system"
            content = f"Image analysis: {content}"
        else:
            role = "system"
        formatted_history.append({"role": role, "content": content})
    logging.debug(f"Formatted chat history: {formatted_history}")
    return formatted_history

async def ai_command(ctx: Union[discord.Interaction, discord.Message], message: str, model: Optional[str] = None, max_tokens: Optional[int] = None):
    user_id = ctx.author.id if hasattr(ctx, 'author') else ctx.user.id
    channel_id = ctx.channel.id

    if is_on_cooldown(user_id):
        logging.debug(f"User {user_id} is on cooldown. Command ignored.")
        return

    logging.debug(f"AI command called for user {user_id} in channel {channel_id}")
    
    is_interaction = isinstance(ctx, discord.Interaction)
    if is_interaction:
        await ctx.response.defer(thinking=True)
    
    try:
        ai_prefs = await get_ai_preferences(user_id)
        model = model or ai_prefs[0]
        max_tokens = max_tokens or ai_prefs[1]
        logging.debug(f"AI preferences for user {user_id}: model={model}, max_tokens={max_tokens}")

        personalization = await get_personalization(user_id)
        personalized_message = get_personalized_message(personalization, message)

        # Retrieve chat history for the specific channel
        chat_history = await get_messages_for_channel(channel_id, HISTORY_LIMIT)
        formatted_history = format_chat_history(chat_history)

        # Add the current message to the history
        formatted_history.append({"role": "user", "content": personalized_message})

        bot_response = await chat_with_ai(formatted_history, max_tokens)
        logging.debug(f"Bot response: {bot_response}")

        await insert_message(user_id, channel_id, message, model, 'user')
        await insert_message(CLIENT_ID, channel_id, bot_response, model, 'bot')

        await send_message(ctx, bot_response)
        update_cooldown(user_id)

    except Exception as e:
        logging.error(f"Error in ai_command: {str(e)}", exc_info=True)
        await send_message(ctx, f"Sorry, I encountered an error while processing your request.")

async def send_message(ctx: Union[discord.Interaction, discord.Message], message: str):
    try:
        if isinstance(ctx, discord.Interaction):
            if ctx.response.is_done():
                await ctx.followup.send(message)
            else:
                await ctx.response.send_message(message)
        else:
            await ctx.channel.send(message)
        logging.debug(f"Sent message: {message}")
    except Exception as e:
        logging.error(f"Failed to send message: {str(e)}", exc_info=True)
