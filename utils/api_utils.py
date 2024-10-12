import os
import aiohttp
import replicate

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_ai(message, max_tokens):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/yourusername/your-repo",  # Replace with your GitHub repo or actual domain
        "X-Title": "Discord Image Analysis Bot",  # Replace with your actual bot name
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/chatgpt-4o-latest",
        "messages": [{"role": "user", "content": message}],
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

async def analyze_image(image_url):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/yourusername/your-repo",  # Replace with your GitHub repo or actual domain
        "X-Title": "Discord Image Analysis Bot",  # Replace with your actual bot name
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/chatgpt-4o-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this image and provide a detailed description of what you see."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
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
