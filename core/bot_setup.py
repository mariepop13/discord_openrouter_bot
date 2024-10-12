import os
import discord
from discord.ext import commands
from discord import app_commands
from commands.command_handler import setup_commands
from commands.ai_commands import ai_command
from commands.image_commands import analyze_image_command, generate_image_command, image_generation_help
from commands.general_commands import clear, ping
from dotenv import load_dotenv

def setup_bot():
    print("Setting up bot in bot_setup.py...")
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        print(f"User ID: {bot.user.id}")
        print("Bot is ready!")

        # Generate and print invite link
        print("Generating invite link...")
        client_id = os.getenv('CLIENT_ID')
        if client_id:
            print(f"CLIENT_ID found: {client_id}")
            permissions = discord.Permissions.text()
            invite_link = discord.utils.oauth_url(client_id, permissions=permissions, scopes=("bot", "applications.commands"))
            print(f"\nBot invite link with required permissions:")
            print(invite_link)
        else:
            print("\nWarning: CLIENT_ID not found in .env file. Invite link couldn't be generated.")

        # Sync slash commands
        await bot.tree.sync()
        print("Slash commands synced")

    @bot.tree.command(name="ai", description="Chat with the AI")
    @app_commands.describe(message="Your message to the AI")
    async def ai(interaction: discord.Interaction, message: str):
        await interaction.response.defer()
        await ai_command(interaction, message)

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
    async def help_command(interaction: discord.Interaction):
        help_text = """
        Available commands:
        /ai [message] - Chat with the AI
        /analyze [image] - Analyze an attached image
        /clear - Clear your command history
        /generate_image [prompt] - Generate an image based on a prompt
        /help - Show this help message
        /image_help - Get help with image generation commands
        /ping - Check if the bot is responsive
        /sync - Synchronize slash commands (Admin only)
        """
        await interaction.response.send_message(help_text)

    @bot.tree.command(name="image_help", description="Get help with image generation commands")
    async def image_help_command(interaction: discord.Interaction):
        await interaction.response.defer()
        await image_generation_help(interaction)

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        await interaction.response.defer()
        await ping(interaction)

    @bot.tree.command(name="sync", description="Synchronize slash commands (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            synced = await bot.tree.sync()
            await interaction.followup.send(f"Synced {len(synced)} commands.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred while syncing commands: {str(e)}", ephemeral=True)

    setup_commands(bot)
    print("Bot setup completed in bot_setup.py")
    return bot
