import os
import aiohttp
import replicate

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_ai(messages, max_tokens):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",  # Replace with your GitHub repo or actual domain
        "X-Title": os.getenv('BOT_NAME'),
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-flash-1.5",
        "messages": messages,
        "max_tokens": max_tokens
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Sorry, I couldn't process your request. Status code: {response.status}"

async def generate_image(prompt):
    output = replicate.run(
        "black-forest-labs/flux-1.1-pro",
        input={"prompt": prompt, "prompt_upsampling": True}
    )
    return output

async def analyze_image(image_url, chat_history=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/mariepop13/discord_openrouter_bot",  # Replace with your GitHub repo or actual domain
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

    data = {
        "model": "openai/chatgpt-4o-latest",
        "messages": messages,
        "max_tokens": 300
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['choices'][0]['message']['content']
                elif response.status == 401:
                    return "Error 401: Unauthorized. Please check your API key and ensure it's valid."
                else:
                    return f"Sorry, I couldn't analyze the image. Status code: {response.status}"
    except Exception as e:
        return f"An error occurred while analyzing the image: {str(e)}"
