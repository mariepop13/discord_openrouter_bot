import aiohttp
from config import OPENROUTER_URL, IMAGE_ANALYSIS_MODEL
from config import get_headers

async def analyze_image(image_url, chat_history=None):
    headers = get_headers()

    messages = chat_history or []
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this image and provide a detailed description of what you see. If there's any relevant context from our previous conversation, please take that into account in your analysis. Reponds dans la langue préceédente (respond in the previous language)."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    })

    analyze_data = {
        "model": IMAGE_ANALYSIS_MODEL,
        "messages": messages
    }

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
