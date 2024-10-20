import discord
from discord import app_commands
from src.commands.ai_preferences import update_ai_settings
from src.commands.ai_chat import ai_command
from src.utils.models import CHAT_MODELS
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class AIOption(discord.Enum):
    personality = "personality"
    tone = "tone"
    language = "language"
    prebuild = "prebuild"
    max_tokens = "max_tokens"
    custom = "custom"

def register_ai_commands(bot):
    @bot.tree.command(name="ai", description="Chat with the AI")
    @app_commands.describe(message="Your message to the AI")
    async def ai_command_wrapper(interaction: discord.Interaction, message: str):
        logger.debug(f"Received /ai command with message: {message}")
        try:
            await ai_command(interaction, message)
        except discord.errors.NotFound:
            logger.warning(f"Interaction not found for user {interaction.user.id}. It may have already been responded to or timed out.")
            # Attempt to send a follow-up message if the original interaction is no longer valid
            try:
                await interaction.followup.send("Sorry, there was a delay in processing your request. Please try again.", ephemeral=True)
            except discord.errors.HTTPException:
                logger.error("Failed to send follow-up message after interaction not found error.")
        except Exception as e:
            logger.error(f"Error in ai_command_wrapper: {str(e)}", exc_info=True)
            try:
                await interaction.followup.send("An error occurred while processing your request. Please try again later.", ephemeral=True)
            except discord.errors.HTTPException:
                logger.error("Failed to send error message to user.")

    @bot.tree.command(name="update_ai_settings", description="Update AI settings")
    @app_commands.describe(
        option="The AI option to set (optional)",
        value="The value to set for the chosen option (optional)",
        model="The AI model to use",
        custom_option="If 'custom' is selected, specify the custom option here"
    )
    @app_commands.choices(model=[app_commands.Choice(name=model, value=model) for model in CHAT_MODELS])
    async def update_ai_settings_wrapper(
        interaction: discord.Interaction, 
        model: Optional[str] = None,
        option: Optional[AIOption] = None,
        value: Optional[str] = None,
        custom_option: Optional[str] = None
    ):
        option_value = custom_option if option == AIOption.custom else option.value if option else None
        logger.debug(f"Received /update_ai_settings command with model: {model}, option: {option}, value: {value}, custom_option: {custom_option}")
        await update_ai_settings(interaction, option_value, value, model)

    @bot.tree.command(name="models", description="List available AI models")
    async def list_models(interaction: discord.Interaction):
        model_list = "\n".join([f"- {model.split('/')[-1]}" for model in CHAT_MODELS])
        await interaction.response.send_message(f"Available models:\n{model_list}")
        logger.debug("Listed available models.")
