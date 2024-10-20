import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Discord Configuration
MAX_MESSAGE_LENGTH = 500
MAX_EMBED_LENGTH = 4000
MESSAGES_PER_PAGE = 5

# AI Model Configuration
DEFAULT_CHAT_MODEL = "google/gemini-flash-1.5"
DEFAULT_IMAGE_ANALYSIS_MODEL = "openai/chatgpt-4o-latest"
DEFAULT_MAX_OUTPUT = 150

def load_env_value(env_var, default):
    value = os.getenv(env_var)
    if value is None:
        return default
    if isinstance(default, int):
        try:
            return int(value)
        except ValueError:
            return default
    return value

# Environment variables
CLIENT_ID = load_env_value('CLIENT_ID', 0)
DISCORD_TOKEN = load_env_value('DISCORD_TOKEN', None)
OPENROUTER_API_KEY = load_env_value('OPENROUTER_API_KEY', None)
REPLICATE_API_TOKEN = load_env_value('REPLICATE_API_TOKEN', None)
LOG_FILES_TO_KEEP = load_env_value('LOG_FILES_TO_KEEP', 5)  # Default to keeping 5 log files
BOT_NAME = load_env_value('BOT_NAME', 'Discord OpenRouter Bot')
HISTORY_LIMIT = load_env_value('HISTORY_LIMIT', 10)  # Default to 10 messages in history

CHAT_MODEL = load_env_value('CHAT_MODEL', DEFAULT_CHAT_MODEL)
IMAGE_ANALYSIS_MODEL = load_env_value('IMAGE_ANALYSIS_MODEL', DEFAULT_IMAGE_ANALYSIS_MODEL)

# Chat Data Configuration
CHAT_DATA = {
    "model": CHAT_MODEL,
    "max_tokens": DEFAULT_MAX_OUTPUT
}

# Header Configuration
def get_headers():
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",
        "X-Title": BOT_NAME,
        "Content-Type": "application/json"
    }
