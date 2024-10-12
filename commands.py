import discord
from discord import app_commands
from api_utils import chat_with_ai, generate_image
from database import insert_message, get_personalization, set_personalization, get_history
from models import MODELS

def setup_commands(bot):
    @bot.tree.command(name="ai", description="Interact with the AI (chat, set personality, generate image, etc.)")
    @app_commands.describe(
        action="The action to perform (chat, set_personality, set_tone, set_language, generate_image)",
        message="The message for chat or prompt for image generation",
        model="The AI model to use for chat (default: google/gemini-flash-1.5)",
        personality="The personality for the AI to adopt",
        tone="The tone for the AI to use",
        language="The language for the AI to use",
        max_tokens="Maximum number of tokens for the response (default: 150)"
    )
    @app_commands.choices(model=[
        app_commands.Choice(name=model.split('/')[-1], value=model)
        for model in MODELS
    ])
    async def ai(
        interaction: discord.Interaction, 
        action: str,
        message: str = None,
        model: str = "google/gemini-flash-1.5",
        personality: str = None,
        tone: str = None,
        language: str = None,
        max_tokens: int = 150
    ):
        await interaction.response.defer()

        if action == "chat":
            personalization = get_personalization(bot.db_cursor, interaction.user.id)
            
            if personalization:
                pers, tn, lang = personalization
                message = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {message}"

            insert_message(bot.db_cursor, interaction.user.id, message, model)
            bot.db_conn.commit()

            bot_response = await chat_with_ai(model, message, max_tokens)
            await interaction.followup.send(bot_response)

        elif action in ["set_personality", "set_tone", "set_language"]:
            value = personality if action == "set_personality" else tone if action == "set_tone" else language
            if value:
                set_personalization(bot.db_cursor, interaction.user.id, action.split('_')[1], value)
                bot.db_conn.commit()
                await interaction.followup.send(f"AI {action.split('_')[1]} set to: {value}")
            else:
                await interaction.followup.send(f"Please provide a {action.split('_')[1]}.")

        elif action == "generate_image":
            if message:
                try:
                    output = await generate_image(message)
                    await interaction.followup.send(f"Generated image: {output}")
                except Exception as e:
                    await interaction.followup.send(f"Sorry, I couldn't generate the image. Error: {str(e)}")
            else:
                await interaction.followup.send("Please provide a prompt for image generation.")

        else:
            await interaction.followup.send("Invalid action. Please use 'chat', 'set_personality', 'set_tone', 'set_language', or 'generate_image'.")

    @bot.tree.command(name="history", description="Get your chat history")
    @app_commands.describe(limit="Number of messages to retrieve (default: 5)")
    async def history(interaction: discord.Interaction, limit: int = 5):
        messages = get_history(bot.db_cursor, interaction.user.id, limit)
        
        if messages:
            history = "\n".join([f"- [{msg[1]}] {msg[0]}" for msg in messages])
            await interaction.response.send_message(f"Your last {limit} messages:\n{history}")
        else:
            await interaction.response.send_message(f"You don't have any message history.")

    @bot.tree.command(name="models", description="List available AI models")
    async def list_models(interaction: discord.Interaction):
        model_list = "\n".join([f"- {model.split('/')[-1]}" for model in MODELS])
        await interaction.response.send_message(f"Available models:\n{model_list}")
