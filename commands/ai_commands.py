import discord
from utils.api_utils import chat_with_ai, generate_image, analyze_image
from utils.database import insert_message, get_personalization, set_personalization, get_ai_preferences, set_ai_preferences
import sqlite3

DB_PATH = 'bot_database.db'  # Adjust this path if necessary

async def analyze_image_command(ctx, image: discord.Attachment):
    try:
        image_url = image.url
        description = await analyze_image(image_url)
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(f"Image analysis: {description}")
        else:
            await ctx.send(f"Image analysis: {description}")
    except Exception as e:
        error_message = f"Sorry, I couldn't analyze the image. Error: {str(e)}"
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(error_message)
        else:
            await ctx.send(error_message)

async def ai_command(interaction: discord.Interaction, model: str = None, max_tokens: int = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        personalization = get_personalization(cursor, interaction.user.id)
        ai_prefs = get_ai_preferences(cursor, interaction.user.id)
        
        model = model or ai_prefs[0]
        max_tokens = max_tokens or ai_prefs[1]

        # Get the message from the user's input after the command
        message = interaction.message.content if interaction.message else ""
        
        if personalization:
            pers, tn, lang, _, _ = personalization
            message = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {message}"

        insert_message(cursor, interaction.user.id, message, model)
        conn.commit()

        bot_response = await chat_with_ai(model, message, max_tokens)
        await interaction.followup.send(bot_response)
    finally:
        conn.close()

async def set_ai_option(interaction: discord.Interaction, option: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        if option in ['personality', 'tone', 'language']:
            set_personalization(cursor, interaction.user.id, option, value)
        elif option == 'model':
            set_ai_preferences(cursor, interaction.user.id, ai_model=value)
        elif option == 'max_tokens':
            try:
                max_tokens = int(value)
                set_ai_preferences(cursor, interaction.user.id, max_output=max_tokens)
            except ValueError:
                await interaction.response.send_message("Error: max_tokens must be an integer.")
                return
        else:
            await interaction.response.send_message(f"Invalid option: {option}")
            return
        
        conn.commit()
        await interaction.response.send_message(f"AI {option} set to: {value}")
    finally:
        conn.close()

async def set_ai_preferences_command(interaction: discord.Interaction, model: str = None, max_tokens: int = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        set_ai_preferences(cursor, interaction.user.id, ai_model=model, max_output=max_tokens)
        conn.commit()
        
        response = "AI preferences updated:"
        if model:
            response += f" Model set to {model}."
        if max_tokens:
            response += f" Max tokens set to {max_tokens}."
        
        await interaction.response.send_message(response)
    finally:
        conn.close()
