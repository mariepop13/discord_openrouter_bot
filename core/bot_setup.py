import os
import discord
from discord.ext import commands
from discord import app_commands
from commands.command_handler import setup_commands
from commands.ai_commands import analyze_image_command
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

    @bot.tree.command(name="analyze", description="Analyze an attached image")
    async def analyze(interaction: discord.Interaction, image: discord.Attachment):
        if not image.content_type.startswith('image/'):
            await interaction.response.send_message("The uploaded file is not an image. Please upload an image file.")
            return

        await interaction.response.defer()
        await analyze_image_command(interaction, image)

    setup_commands(bot)
    print("Bot setup completed in bot_setup.py")
    return bot
