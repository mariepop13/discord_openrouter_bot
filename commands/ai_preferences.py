from typing import Literal
import discord
from utils.database import set_personalization, set_ai_preferences

# Constants for option names
PERSONALITY = 'personality'
TONE = 'tone'
LANGUAGE = 'language'
PREBUILD = 'prebuild'
MODEL = 'model'
MAX_TOKENS = 'max_tokens'

OptionType = Literal[PERSONALITY, TONE, LANGUAGE, PREBUILD, MODEL, MAX_TOKENS]

async def set_ai_preferences_command(interaction: discord.Interaction, option: OptionType, value: str):
    try:
        if option in [PERSONALITY, TONE, LANGUAGE, PREBUILD]:
            set_personalization(interaction.user.id, option, value)
        elif option == MODEL:
            set_ai_preferences(interaction.user.id, ai_model=value)
        elif option == MAX_TOKENS:
            try:
                max_tokens = int(value)
                set_ai_preferences(interaction.user.id, max_output=max_tokens)
            except ValueError:
                await interaction.response.send_message("Error: max_tokens must be an integer.", ephemeral=True)
                return
        else:
            await interaction.response.send_message(f"Invalid option: {option}", ephemeral=True)
            return
        
        await interaction.response.send_message(f"AI {option} set to: {value}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred while setting AI preferences: {str(e)}", ephemeral=True)
