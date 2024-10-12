import os
import sys
import logging
from dotenv import load_dotenv
from core.bot_setup import setup_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Starting bot initialization...")

# Load environment variables
load_dotenv()

logging.info("Environment variables loaded.")

# Setup the bot
logging.info("Setting up bot...")
bot = setup_bot()

token = os.getenv('DISCORD_TOKEN')
if not token:
    logging.error("Error: DISCORD_TOKEN not found in .env file")
else:
    logging.info("DISCORD_TOKEN found. Attempting to run bot...")

    try:
        bot.run(token)
    except KeyboardInterrupt:
        logging.info("Bot execution interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred while running the bot: {e}")

logging.info("Bot script execution completed.")

print("Bot has been shut down. You can close this window.")
