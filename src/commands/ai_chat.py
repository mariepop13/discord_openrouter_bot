import discord
from typing import Union, Optional
import logging
import os

from src.utils.chat_utils import chat_with_ai
from src.database.database_operations import get_personalization, get_ai_preferences
from src.database.message_insertion import insert_message
from src.database.channel_messages import get_messages_for_channel
from src.commands.cooldown import is_on_cooldown, update_cooldown
from src.utils.message_utils import get_personalized_message, format_chat_history
from src.utils.discord_utils import send_message, get_user_id, get_channel_id, is_interaction

CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT'))

async def ai_command(ctx: Union[discord.Interaction, discord.Message], message: str, model: Optional[str] = None, max_tokens: Optional[int] = None):
    user_id = get_user_id(ctx)
    channel_id = get_channel_id(ctx)

    if is_on_cooldown(user_id):
        logging.debug(f"User {user_id} is on cooldown. Command ignored.")
        return

    logging.debug(f"AI command called for user {user_id} in channel {channel_id}")
    
    if is_interaction(ctx):
        try:
            await ctx.response.defer(thinking=True)
        except discord.errors.NotFound:
            logging.warning(f"Interaction not found for user {user_id}. It may have already been responded to or timed out.")
            return
        except Exception as e:
            logging.error(f"Error deferring interaction: {str(e)}", exc_info=True)
            return
    
    try:
        ai_prefs = await get_ai_preferences(user_id)
        model = model or ai_prefs[0]
        max_tokens = max_tokens or ai_prefs[1]
        logging.debug(f"AI preferences for user {user_id}: model={model}, max_tokens={max_tokens}")

        personalization = await get_personalization(user_id)
        personalized_message = get_personalized_message(personalization, message)

        chat_history = await get_messages_for_channel(channel_id, HISTORY_LIMIT)
        formatted_history = format_chat_history(chat_history)

        formatted_history.append({"role": "user", "content": personalized_message})

        # Check if the message starts with @bot or if it's an /ai command
        should_mention_user = message.startswith('@bot') or (is_interaction(ctx) and ctx.command.name == 'ai')

        bot_response = await chat_with_ai(formatted_history, max_tokens)
        logging.debug(f"Bot response: {bot_response}")

        # If the user used @bot or /ai, prepend the response with @personne
        mentioned_user_id = None
        if should_mention_user:
            user_mention = f"<@{user_id}>"
            bot_response = f"{user_mention} {bot_response}"
            mentioned_user_id = user_id

        await insert_message(user_id, channel_id, message, model, 'user')
        await insert_message(CLIENT_ID, channel_id, bot_response, model, 'bot', mentioned_user_id)

        await send_message(ctx, bot_response)
        update_cooldown(user_id)

    except Exception as e:
        logging.error(f"Error in ai_command: {str(e)}", exc_info=True)
        await send_message(ctx, f"Sorry, I encountered an error while processing your request.")
