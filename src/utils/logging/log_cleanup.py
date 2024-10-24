import os
import glob
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def cleanup_logs(log_dir='logs', keep_latest=None):
    """
    Cleans up log files by keeping only the most recent ones.
    
    :param log_dir: The directory containing the log files
    :param keep_latest: The number of log files to keep (overrides .env value if provided)
    """
    logger.debug(f"Current working directory: {os.getcwd()}")
    dotenv_path = Path('.env')
    logger.debug(f"Loading .env file from: {dotenv_path.absolute()}")
    
    # Load .env file
    load_dotenv(dotenv_path)
    
    # Explicitly read from .env file
    env_value = os.getenv('LOG_FILES_TO_KEEP')
    logger.debug(f"LOG_FILES_TO_KEEP from os.environ: {env_value}")
    
    # Use the value from .env if keep_latest is not provided
    if keep_latest is None:
        keep_latest = int(env_value) if env_value is not None else 5
    
    logger.info(f"Keeping {keep_latest} most recent log files")
    
    # Full path to the log directory
    log_path = Path(log_dir)
    
    # List all .log files in the directory
    log_files = glob.glob(str(log_path / '*.log'))
    
    # Sort files by modification time (newest first)
    sorted_files = sorted(log_files, key=os.path.getmtime, reverse=True)
    
    # Keep the most recent files
    files_to_keep = sorted_files[:keep_latest]
    
    # Remove the remaining files
    for file in sorted_files[keep_latest:]:
        try:
            os.remove(file)
            logger.info(f"File deleted: {file}")
        except Exception as e:
            logger.error(f"Error deleting {file}: {e}")
    
    logger.info("Log cleanup completed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cleanup_logs()
