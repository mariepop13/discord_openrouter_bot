import logging
import os
from logging.handlers import RotatingFileHandler

class BotReadyFilter(logging.Filter):
    def filter(self, record):
        return "Bot is ready" in record.msg

class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

def setup_logging(log_file_path):
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Configure the root logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Create a rotating file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    console_handler.addFilter(ConsoleFilter())

    # Get the root logger and add the handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Remove any existing StreamHandlers to avoid duplicate logs
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler != console_handler:
            root_logger.removeHandler(handler)

    # Configure discord library logging
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.ERROR)

    return root_logger

def get_logger(name):
    logger = logging.getLogger(name)
    return logger
