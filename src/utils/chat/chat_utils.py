import aiohttp
import logging
from config import OPENROUTER_URL, CHAT_MODEL, get_headers

async def chat_with_ai(messages, model=None, max_tokens=None):
    headers = get_headers()
    chat_data = {
        "model": model or CHAT_MODEL["model"],
        "messages": messages
    }
    if max_tokens:
        chat_data["max_tokens"] = max_tokens
    else:
        chat_data["max_tokens"] = CHAT_MODEL["max_tokens"]

    # Log the chat_data to verify its content
    logging.debug(f"Chat data being sent: {chat_data}")

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=chat_data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Sorry, I couldn't process your request. Status code: {response.status}"
