import logging
import os
from logging.handlers import RotatingFileHandler
from colorama import Fore, Back, Style, init

init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Back.WHITE + Style.BRIGHT,
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, '')}{log_message}{Style.RESET_ALL}"

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return True  # Allow all messages, we'll handle filtering in the formatter

def setup_logging(log_file_path, use_color=False):
    print("console.log starting")

    # Configure the root logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.addFilter(ConsoleFilter())

    if use_color:
        formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(formatter)

    # Get the root logger and add the handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # Configure discord library logging
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)

    return root_logger

def get_logger(name):
    return logging.getLogger(name)
