from typing import Optional
import discord
from utils.database_operations import set_personalization, set_ai_preferences
from utils.models import MODELS

# Constants for option names
PERSONALITY = 'personality'
TONE = 'tone'
LANGUAGE = 'language'
PREBUILD = 'prebuild'
MAX_TOKENS = 'max_tokens'

async def update_ai_settings(interaction: discord.Interaction, option: Optional[str] = None, value: Optional[str] = None, model: Optional[str] = None):
    try:
        if model is not None:
            if model in MODELS or '/' in model:  # Check if it's a valid model from the list or a custom OpenRouter string
                await set_ai_preferences(interaction.user.id, ai_model=model)
                await interaction.response.send_message(f"AI model set to: {model}", ephemeral=True)
            else:
                await interaction.response.send_message("Error: Invalid model selection.", ephemeral=True)
                return

        if option is not None and value is not None:
            if option in [PERSONALITY, TONE, LANGUAGE, PREBUILD]:
                await set_personalization(interaction.user.id, option, value)
                await interaction.response.send_message(f"AI {option} set to: {value}", ephemeral=True)
            elif option == MAX_TOKENS:
                try:
                    max_tokens = int(value)
                    await set_ai_preferences(interaction.user.id, max_output=max_tokens)
                    await interaction.response.send_message(f"AI max tokens set to: {max_tokens}", ephemeral=True)
                except ValueError:
                    await interaction.response.send_message("Error: max_tokens must be an integer.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Invalid option: {option}", ephemeral=True)
        
        elif option is not None or value is not None:
            await interaction.response.send_message("Error: Both option and value must be provided together.", ephemeral=True)
        
        elif model is None:
            await interaction.response.send_message("Error: No changes were made. Please provide a model or both option and value.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"An error occurred while updating AI settings: {str(e)}", ephemeral=True)
