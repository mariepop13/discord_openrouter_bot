import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from src.core.bot import run_bot
from src.utils.logging_utils import setup_logging, get_logger
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

async def main():
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Set up the log file
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', f'app_{timestamp}.log')
    
    setup_logging(log_file, use_color=True)
    logger = get_logger(__name__)
    logger.debug("Starting bot initialization...")
    
    load_dotenv()
    
    await run_bot()
    
    logger.debug("Bot script execution completed.")
    print(Fore.GREEN + "Bot has been shut down. You can close this window.")

if __name__ == "__main__":
    asyncio.run(main())
