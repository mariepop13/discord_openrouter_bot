from datetime import datetime
from src.config import MAX_MESSAGE_LENGTH

def format_message(message_user_id, content, model, message_type, timestamp):
    formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    
    if message_type == 'user':
        icon = "🧑"
        sender = "You"
    elif message_type == 'bot' and model == 'image_analysis':
        icon = "🖼️"
        sender = "Image Analysis"
    elif message_type == 'bot':
        icon = "🤖"
        sender = f"AI ({model})"
    else:
        icon = "❓"
        sender = "Unknown"
    
    formatted_message = f"{icon} **{sender}** - {formatted_time}\n{content[:MAX_MESSAGE_LENGTH]}"
    if len(content) > MAX_MESSAGE_LENGTH:
        formatted_message += "\n*(Message truncated)*"
    
    return formatted_message
