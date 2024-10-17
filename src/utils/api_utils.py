import os
import json
import aiohttp
import replicate
import uuid
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Définition des valeurs par défaut
DEFAULT_CHAT_DATA = {"model": "google/gemini-flash-1.5"}
DEFAULT_ANALYZE_DATA = {"model": "openai/chatgpt-4o-latest"}

# Chargement des variables d'environnement avec gestion des erreurs
def load_env_json(env_var, default):
    try:
        return json.loads(os.getenv(env_var, 'null')) or default
    except json.JSONDecodeError:
        logger.error(f"JSON decoding error for {env_var}. Using default value.")
        return default

CHAT_DATA = load_env_json('CHAT_DATA', DEFAULT_CHAT_DATA)
ANALYZE_DATA = load_env_json('ANALYZE_DATA', DEFAULT_ANALYZE_DATA)

async def chat_with_ai(messages, max_tokens=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",
        "X-Title": os.getenv('BOT_NAME'),
        "Content-Type": "application/json"
    }
    chat_data = CHAT_DATA.copy()
    chat_data["messages"] = messages
    if max_tokens:
        chat_data["max_tokens"] = max_tokens

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=chat_data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Sorry, I couldn't process your request. Status code: {response.status}"

async def generate_image(prompt, model="black-forest-labs/flux-dev"):
    logger.debug(f"Generating image with prompt: {prompt}, model: {model}")
    try:
        output = await replicate.async_run(
            model,
            input={"prompt": prompt}
        )
        logger.debug(f"Raw output for {model}: {output}")
        
        if model == "black-forest-labs/flux-1.1-pro":
            if isinstance(output, list) and len(output) > 0:
                return output[0]
            elif isinstance(output, str):
                return output
            else:
                logger.warning(f"Unexpected output format from Replicate API for flux-1.1-pro: {output}")
                return str(output)
        else:
            if isinstance(output, list) and len(output) > 0:
                # Generate a unique filename
                filename = f"{uuid.uuid4()}.webp"
                filepath = Path("generated_images") / filename
                
                # Ensure the directory exists
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the image locally
                with open(filepath, 'wb') as file:
                    file.write(output[0].read())
                
                # Return the local file path and the URL
                return {
                    "local_path": str(filepath),
                    "url": output[0].url
                }
            else:
                logger.warning(f"Unexpected output format from Replicate API: {output}")
                return str(output)
    except Exception as e:
        logger.error(f"An error occurred during image generation: {str(e)}")
        return f"An error occurred during image generation: {str(e)}"

async def analyze_image(image_url, chat_history=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",
        "X-Title": os.getenv('BOT_NAME'),
        "Content-Type": "application/json"
    }

    messages = chat_history or []
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this image and provide a detailed description of what you see. If there's any relevant context from our previous conversation, please take that into account in your analysis. Reponds dans la langue préceédente (respond in the previous language)."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    })

    analyze_data = ANALYZE_DATA.copy()
    analyze_data["messages"] = messages

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=analyze_data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                elif response.status == 401:
                    return "Error 401: Unauthorized. Please check your API key and ensure it's valid."
                else:
                    return f"Sorry, I couldn't analyze the image. Status code: {response.status}"
    except Exception as e:
        return f"An error occurred while analyzing the image: {str(e)}"
