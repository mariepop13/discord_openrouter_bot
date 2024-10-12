import discord
from utils.api_utils import chat_with_ai
from utils.database import setup_database, insert_message, get_personalization, get_ai_preferences
import logging
import traceback

async def ai_command(ctx, message: str, model: str = None, max_tokens: int = None):
    logging.info(f"AI command called with message: {message}")
    
    conn, cursor = setup_database()
    try:
        user_id = ctx.author.id if hasattr(ctx, 'author') else ctx.user.id
        logging.info(f"User ID: {user_id}")
        
        personalization = get_personalization(cursor, user_id)
        ai_prefs = get_ai_preferences(cursor, user_id)
        
        model = model or ai_prefs[0]
        max_tokens = max_tokens or ai_prefs[1]

        logging.info(f"Using model: {model}, max_tokens: {max_tokens}")
        
        if personalization:
            pers, tn, lang, _, _ = personalization
            message = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {message}"

        insert_message(cursor, user_id, message, model)
        conn.commit()
    except Exception as db_error:
        logging.error(f"Database error in ai_command: {str(db_error)}")
        logging.error(traceback.format_exc())
    finally:
        conn.close()

    try:
        bot_response = await chat_with_ai(message, max_tokens)
        logging.info(f"AI response generated: {bot_response[:50]}...")  # Log first 50 chars of response
        
        if isinstance(ctx, discord.Interaction):
            logging.info("Sending response via Interaction.followup.send")
            await ctx.followup.send(bot_response)
        else:
            logging.info("Sending response via channel.send")
            await ctx.channel.send(bot_response)
        logging.info("Response sent successfully")
    except discord.errors.HTTPException as http_err:
        logging.error(f"HTTP error when sending message: {http_err}")
        await ctx.channel.send(f"An error occurred while sending the message: {http_err}")
    except discord.errors.Forbidden as forbid_err:
        logging.error(f"Forbidden error: Bot doesn't have permission to send messages: {forbid_err}")
    except Exception as e:
        error_message = f"Sorry, I encountered an error while processing your request. Error: {str(e)}"
        logging.error(f"Error in ai_command: {str(e)}")
        logging.error(traceback.format_exc())
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(error_message)
        else:
            await ctx.channel.send(error_message)
