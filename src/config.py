import os

# API Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Discord Configuration
MAX_MESSAGE_LENGTH = 500
MAX_EMBED_LENGTH = 4000
MESSAGES_PER_PAGE = 5

# AI Model Configuration
DEFAULT_CHAT_MODEL = "google/gemini-flash-1.5"
DEFAULT_IMAGE_ANALYSIS_MODEL = "openai/chatgpt-4o-latest"
DEFAULT_MAX_OUTPUT = 150

# Environment variables
CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
LOG_FILES_TO_KEEP = int(os.getenv('LOG_FILES_TO_KEEP', '5'))
BOT_NAME = os.getenv('BOT_NAME', 'Discord OpenRouter Bot')
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT', '30'))

def load_env_value(env_var, default):
    return os.getenv(env_var, default)

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
