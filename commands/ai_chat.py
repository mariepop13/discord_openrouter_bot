import discord
from utils.api_utils import chat_with_ai
from utils.database import get_personalization, get_ai_preferences, insert_message
import logging
import os
from collections import defaultdict
import time
from typing import Union, Optional

# These could be moved to a config file
CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
COOLDOWN_TIME = 5  # Cooldown time in seconds

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
        bot_response = await chat_with_ai(personalized_message, max_tokens)

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
