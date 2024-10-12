import discord
from discord import app_commands
from commands.ai_preferences import set_ai_preferences_command
from commands.image_commands import analyze_image_command, generate_image_command, image_generation_help
from commands.general_commands import clear, ping
from commands.history_command import history
from core.help_command import help_command
from utils.models import MODELS
from typing import Optional

class AIOption(discord.Enum):
    personality = "personality"
    tone = "tone"
    language = "language"
    prebuild = "prebuild"
    model = "model"
    max_tokens = "max_tokens"
    custom = "custom"

def register_commands(bot):
    @bot.tree.command(name="set_ai_preferences", description="Set AI preferences")
    @app_commands.describe(
        option="The AI option to set",
        value="The value to set for the chosen option",
        custom_option="If 'custom' is selected, specify the custom option here"
    )
    async def set_ai_preferences_wrapper(
        interaction: discord.Interaction, 
        option: AIOption,
        value: str,
        custom_option: Optional[str] = None
    ):
        if option == AIOption.custom:
            if custom_option is None:
                await interaction.response.send_message("Please provide a custom option when selecting 'custom'.", ephemeral=True)
                return
            option = custom_option
        else:
            option = option.value
        
        await set_ai_preferences_command(interaction, option, value)

    @bot.tree.command(name="analyze", description="Analyze an attached image")
    async def analyze(interaction: discord.Interaction, image: discord.Attachment):
        if not image.content_type.startswith('image/'):
            await interaction.response.send_message("The uploaded file is not an image. Please upload an image file.")
            return

        await interaction.response.defer()
        await analyze_image_command(interaction, image)

    @bot.tree.command(name="clear", description="Clear your command history")
    async def clear_command(interaction: discord.Interaction):
        await interaction.response.defer()
        await clear(interaction)

    @bot.tree.command(name="generate_image", description="Generate an image based on a prompt")
    @app_commands.describe(prompt="Your image generation prompt")
    async def generate_image(interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        await generate_image_command(interaction, prompt, bot)

    @bot.tree.command(name="help", description="Get information about available commands")
    async def help_command_wrapper(interaction: discord.Interaction):
        await help_command(interaction)

    @bot.tree.command(name="image_help", description="Get help with image generation commands")
    async def image_help_command(interaction: discord.Interaction):
        await interaction.response.defer()
        await image_generation_help(interaction)

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        await interaction.response.defer()
        await ping(interaction)

    # Register the new history command
    bot.tree.add_command(history)
