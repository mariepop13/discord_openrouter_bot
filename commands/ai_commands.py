import discord
from utils.api_utils import chat_with_ai, generate_image, analyze_image
from utils.database import insert_message, get_personalization, set_personalization

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

async def ai_command(interaction: discord.Interaction, message: str):
    bot = interaction.client
    personalization = get_personalization(bot.db_cursor, interaction.user.id)
    
    if personalization:
        pers, tn, lang = personalization
        message = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {message}"

    insert_message(bot.db_cursor, interaction.user.id, message, "google/gemini-flash-1.5")
    bot.db_conn.commit()

    bot_response = await chat_with_ai("google/gemini-flash-1.5", message, 150)
    await interaction.followup.send(bot_response)

async def set_ai_option(interaction: discord.Interaction, option: str, value: str):
    bot = interaction.client
    set_personalization(bot.db_cursor, interaction.user.id, option, value)
    bot.db_conn.commit()
    await interaction.response.send_message(f"AI {option} set to: {value}")
