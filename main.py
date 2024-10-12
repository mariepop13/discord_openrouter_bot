import os
from dotenv import load_dotenv
from bot_setup import setup_bot

# Load environment variables
load_dotenv()

# Setup and run the bot
bot = setup_bot()
bot.run(os.getenv('DISCORD_TOKEN'))
