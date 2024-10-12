import discord
from utils.api_utils import chat_with_ai
from utils.database_operations import get_personalization, get_ai_preferences, insert_message, get_history
import logging
import os
from collections import defaultdict
import time
from typing import Union, Optional

# These could be moved to a config file
CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
COOLDOWN_TIME = 5  # Cooldown time in seconds
HISTORY_LIMIT = 20  # Number of previous messages to include for context

last_response_time = defaultdict(float)

def is_on_cooldown(user_id: int) -> bool:
    return time.time() - last_response_time[user_id] < COOLDOWN_TIME

def update_cooldown(user_id: int) -> None:
    last_response_time[user_id] = time.time()

def get_personalized_message(personalization: tuple, message: str) -> str:
    if not personalization:
        return message

    pers, tn, lang, _, _ = personalization
    parts = [f"a {pers} personality" if pers else None,
             f"a {tn} tone" if tn else None,
             f"in {lang} language" if lang else None]
    parts = [p for p in parts if p]
    
    if parts:
        return f"Please respond with {', '.join(parts)}. User message: {message}"
    return message

def format_chat_history(history):
    formatted_history = []
    for _, content, _, message_type, _ in history:
        role = "user" if message_type == "user" else "assistant"
        formatted_history.append({"role": role, "content": content})
    return formatted_history

async def ai_command(ctx: Union[discord.Interaction, discord.Message], message: str, model: Optional[str] = None, max_tokens: Optional[int] = None):
    user_id = ctx.author.id if hasattr(ctx, 'author') else ctx.user.id

    if is_on_cooldown(user_id):
        return

    logging.info(f"AI command called for user {user_id}")
    
    is_interaction = isinstance(ctx, discord.Interaction)
    if is_interaction:
        await ctx.response.defer(thinking=True)
    
    try:
        ai_prefs = await get_ai_preferences(user_id)
        model = model or ai_prefs[0]
        max_tokens = max_tokens or ai_prefs[1]

        personalization = await get_personalization(user_id)
        personalized_message = get_personalized_message(personalization, message)

        # Retrieve chat history
        chat_history = await get_history(user_id, HISTORY_LIMIT)
        formatted_history = format_chat_history(chat_history)

        # Add the current message to the history
        formatted_history.append({"role": "user", "content": personalized_message})

        bot_response = await chat_with_ai(formatted_history, max_tokens)

        await insert_message(user_id, message, model, 'user')
        await insert_message(CLIENT_ID, bot_response, model, 'bot')

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
    except Exception as e:
        logging.error(f"Failed to send message: {str(e)}", exc_info=True)
