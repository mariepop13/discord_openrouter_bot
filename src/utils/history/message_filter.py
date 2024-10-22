import logging

def filter_history(chat_history, filter_type):
    filtered = [
        message for message in chat_history
        if filter_type == 'all' or
        (filter_type == 'chat' and message[3] in ['user', 'bot']) or
        (filter_type == 'image' and message[3] == 'image_analysis')
    ]
    logging.info(f"Filtered history contains {len(filtered)} messages. Filter type: {filter_type}")
    return filtered
