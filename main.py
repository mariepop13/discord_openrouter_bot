import os
from dotenv import load_dotenv
from datetime import datetime
from src.core.bot import run_bot
from src.utils.logging_utils import setup_logging, get_logger

def main():
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Set up the log file
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', f'app_{timestamp}.log')
    
    setup_logging(log_file)
    logger = get_logger(__name__)
    logger.debug("Starting bot initialization...")
    
    load_dotenv()
    
    print("Starting the bot. If you encounter any issues with command visibility, please follow these steps:")
    print("1. Ensure the bot has the necessary permissions in your Discord server.")
    print("2. If commands are not visible after a few minutes, use the '!forcesync' command (bot owner only).")
    print("3. If issues persist, restart the bot and use '!forcesync' again.")
    print("\nNote: There may be a delay between syncing commands and their visibility in Discord.")
    
    run_bot()
    
    logger.debug("Bot script execution completed.")
    print("Bot has been shut down. You can close this window.")

if __name__ == "__main__":
    main()
