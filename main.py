import os
from dotenv import load_dotenv
from core.bot_setup import setup_bot

print("Starting bot initialization...")

# Load environment variables
load_dotenv()

print("Environment variables loaded.")

# Setup the bot
print("Setting up bot...")
bot = setup_bot()

token = os.getenv('DISCORD_TOKEN')
if not token:
    print("Error: DISCORD_TOKEN not found in .env file")
else:
    print("DISCORD_TOKEN found. Attempting to run bot...")

    try:
        bot.run(token)
    except Exception as e:
        print(f"An error occurred while running the bot: {e}")

print("Bot script execution completed.")
