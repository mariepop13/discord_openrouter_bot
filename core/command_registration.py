import discord
from discord import app_commands
from commands.ai_preferences import set_ai_preferences_command
from commands.image_commands import analyze_image_command, generate_image_command, image_generation_help
from commands.general_commands import clear, ping
from core.help_command import help_command
from utils.models import MODELS

def register_commands(bot):
    bot.tree.command(name="set_ai_preferences", description="Set AI preferences")(set_ai_preferences_command)

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
