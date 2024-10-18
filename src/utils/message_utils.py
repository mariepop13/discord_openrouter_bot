import logging

def get_personalized_message(personalization: tuple, message: str) -> str:
    if not personalization:
        logging.debug("No personalization found.")
        return message

    pers, tn, lang, _, _ = personalization
    parts = [f"a {pers} personality" if pers else None,
             f"a {tn} tone" if tn else None,
             f"in {lang} language" if lang else None]
    parts = [p for p in parts if p]
    
    if parts:
        personalized_message = f"Please respond with {', '.join(parts)}. User message: {message}"
        logging.debug(f"Personalized message: {personalized_message}")
        return personalized_message
    return message

def format_chat_history(history):
    formatted_history = []
    for user_id, content, model, message_type, timestamp in history:
        if message_type == "user":
            role = "user"
        elif message_type == "bot":
            role = "assistant"
        elif message_type == "image_analysis":
            role = "system"
            content = f"Image analysis: {content}"
        else:
            role = "system"
        formatted_history.append({"role": role, "content": content})
    logging.debug(f"Formatted chat history: {formatted_history}")
    return formatted_history
