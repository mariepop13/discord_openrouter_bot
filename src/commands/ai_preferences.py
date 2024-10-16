from typing import Optional
import discord
import logging
from src.database.database_operations import set_personalization, set_ai_preferences
from src.utils.models import MODELS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PERSONALITY = 'personality'
TONE = 'tone'
LANGUAGE = 'language'
PREBUILD = 'prebuild'
MAX_TOKENS = 'max_tokens'

async def update_ai_settings(interaction: discord.Interaction, option: Optional[str] = None, value: Optional[str] = None, model: Optional[str] = None):
    try:
        logging.debug(f"User {interaction.user.id} initiated update_ai_settings with option={option}, value={value}, model={model}")

        if model is not None:
            if model in MODELS or '/' in model: 
                await set_ai_preferences(interaction.user.id, ai_model=model)
                await interaction.response.send_message(f"AI model set to: {model}", ephemeral=True)
                logging.debug(f"AI model set to: {model} for user {interaction.user.id}")
            else:
                await interaction.response.send_message("Error: Invalid model selection.", ephemeral=True)
                logging.warning(f"Invalid model selection: {model} by user {interaction.user.id}")
                return

        if option is not None and value is not None:
            if option in [PERSONALITY, TONE, LANGUAGE, PREBUILD]:
                await set_personalization(interaction.user.id, option, value)
                await interaction.response.send_message(f"AI {option} set to: {value}", ephemeral=True)
                logging.debug(f"AI {option} set to: {value} for user {interaction.user.id}")
            elif option == MAX_TOKENS:
                try:
                    max_tokens = int(value)
                    await set_ai_preferences(interaction.user.id, max_output=max_tokens)
                    await interaction.response.send_message(f"AI max tokens set to: {max_tokens}", ephemeral=True)
                    logging.debug(f"AI max tokens set to: {max_tokens} for user {interaction.user.id}")
                except ValueError:
                    await interaction.response.send_message("Error: max_tokens must be an integer.", ephemeral=True)
                    logging.warning(f"Invalid max_tokens value: {value} by user {interaction.user.id}")
            else:
                await interaction.response.send_message(f"Invalid option: {option}", ephemeral=True)
                logging.warning(f"Invalid option: {option} by user {interaction.user.id}")
        
        elif option is not None or value is not None:
            await interaction.response.send_message("Error: Both option and value must be provided together.", ephemeral=True)
            logging.warning(f"Both option and value must be provided together by user {interaction.user.id}")
        
        elif model is None:
            await interaction.response.send_message("Error: No changes were made. Please provide a model or both option and value.", ephemeral=True)
            logging.warning(f"No changes were made by user {interaction.user.id}")

    except Exception as e:
        await interaction.response.send_message(f"An error occurred while updating AI settings: {str(e)}", ephemeral=True)
        logging.error(f"An error occurred while updating AI settings for user {interaction.user.id}: {str(e)}")
