import os
import sys
from dotenv import load_dotenv
from src.core.bot_setup import setup_bot
from src.utils.logging_utils import setup_logging, get_logger

def main():
    # Créer un chemin absolu pour le fichier de log
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
    
    logger = setup_logging(log_file)
    logger.info("Starting bot initialization...")
    
    load_dotenv()
    bot = setup_bot()

    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logger.error("Error: DISCORD_TOKEN not found in .env file")
        return

    try:
        bot.run(token)
    except KeyboardInterrupt:
        logger.info("Bot execution interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}")
    finally:
        logger.info("Bot script execution completed.")
        print("Bot has been shut down. You can close this window.")

if __name__ == "__main__":
    main()
