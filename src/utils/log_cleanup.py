import os
import glob
from pathlib import Path
from dotenv import load_dotenv

def cleanup_logs(log_dir='logs', keep_latest=None):
    """
    Cleans up log files by keeping only the most recent ones.
    
    :param log_dir: The directory containing the log files
    :param keep_latest: The number of log files to keep (overrides .env value if provided)
    """
    load_dotenv()
    
    # Use the value from .env if keep_latest is not provided
    if keep_latest is None:
        keep_latest = int(os.getenv('LOG_FILES_TO_KEEP', 5))
    
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
            print(f"File deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

if __name__ == "__main__":
    cleanup_logs()
