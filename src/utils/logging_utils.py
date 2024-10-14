import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file_path):
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Configure the root logger
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Create a rotating file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Get the root logger and add the file handler
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    return root_logger

def get_logger(name):
    return logging.getLogger(name)
