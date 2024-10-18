import os

# API Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model Configuration
DEFAULT_CHAT_DATA = "google/gemini-flash-1.5"
DEFAULT_ANALYZE_DATA = "openai/chatgpt-4o-latest"

def load_env_value(env_var, default):
    return os.getenv(env_var, default)

CHAT_DATA = load_env_value('CHAT_DATA', DEFAULT_CHAT_DATA)
ANALYZE_DATA = load_env_value('ANALYZE_DATA', DEFAULT_ANALYZE_DATA)

# Header Configuration
def get_headers():
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",
        "X-Title": os.getenv('BOT_NAME'),
        "Content-Type": "application/json"
    }
