import aiohttp
from config import OPENROUTER_URL, CHAT_DATA, get_headers

async def chat_with_ai(messages, max_tokens=None):
    headers = get_headers()
    chat_data = {
        "model": CHAT_DATA,
        "messages": messages
    }
    if max_tokens:
        chat_data["max_tokens"] = max_tokens

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=chat_data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Sorry, I couldn't process your request. Status code: {response.status}"
