import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from commands.ai_chat import ai_command
from commands.image_analysis import analyze_image_command
from commands.ai_preferences import set_ai_option, set_ai_preferences_command
from utils.database import setup_database
import logging

def initialize_bot():
    logging.info("Initializing bot...")
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logging.info(f"Logged in as {bot.user.name}")
        logging.info(f"User ID: {bot.user.id}")
        logging.info("Bot is ready!")

        # Generate and print invite link
        logging.info("Generating invite link...")
        client_id = os.getenv('CLIENT_ID')
        if client_id:
            logging.info(f"CLIENT_ID found: {client_id}")
            permissions = discord.Permissions.text()
            invite_link = discord.utils.oauth_url(client_id, permissions=permissions, scopes=("bot", "applications.commands"))
            logging.info(f"Bot invite link with required permissions:\n{invite_link}")
        else:
            logging.warning("CLIENT_ID not found in .env file. Invite link couldn't be generated.")

        # Sync slash commands
        try:
            synced = await bot.tree.sync()
            logging.info(f'Successfully synced {len(synced)} commands globally.')
        except Exception as e:
            logging.error(f'Error syncing commands: {e}')

    @bot.event
    async def on_message(message):
        if bot.user.mentioned_in(message) and not message.mention_everyone:
            logging.info(f"Bot mentioned in message: {message.content}")
            # Remove the bot mention from the message content
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
            
            try:
                await ai_command(message, content)
            except Exception as e:
                logging.error(f"Error in ai_command: {e}")
                await message.channel.send("Sorry, I encountered an error while processing your request.")
        
        await bot.process_commands(message)

    # Register slash commands
    @bot.tree.command(name="set_ai_option", description="Set AI preferences")
    async def set_option(interaction: discord.Interaction, option: str, value: str):
        await set_ai_option(interaction, option, value)

    return bot
