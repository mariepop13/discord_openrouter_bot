import os
import aiohttp
import replicate

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def chat_with_ai(model, message, max_tokens):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result['choices'][0]['message']['content']
            else:
                return "Sorry, I couldn't process your request."

async def generate_image(prompt):
    output = replicate.run(
        "black-forest-labs/flux-1.1-pro",
        input={"prompt": prompt, "prompt_upsampling": True}
    )
    return output
