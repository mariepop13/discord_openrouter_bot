import os
import sys
from dotenv import load_dotenv
from src.core.bot_setup import setup_bot
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("bot_log.txt"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    configure_logging()
    logging.info("Starting bot initialization...")
    
    load_dotenv()
    bot = setup_bot()

    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logging.error("Error: DISCORD_TOKEN not found in .env file")
        return

    try:
        bot.run(token)
    except KeyboardInterrupt:
        logging.info("Bot execution interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred while running the bot: {e}")
    finally:
        logging.info("Bot script execution completed.")
        print("Bot has been shut down. You can close this window.")

if __name__ == "__main__":
    main()
