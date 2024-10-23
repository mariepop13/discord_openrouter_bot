import logging
from src.utils.message_formatting import format_message
from config import MAX_EMBED_LENGTH

def format_history(filtered_history):
    formatted = "\n\n".join([
        format_message(
            message[0],  # user_id
            message[1],  # content
            message[2],  # model
            message[3],  # message_type
            message[4],  # timestamp
            message[5] if len(message) > 5 else None  # mentioned_user_id (if present)
        ) for message in filtered_history
    ])
    logging.info(f"Formatted {len(filtered_history)} messages for display")
    return formatted

def create_chunks(formatted_history):
    chunks = [formatted_history[i:i+MAX_EMBED_LENGTH] for i in range(0, len(formatted_history), MAX_EMBED_LENGTH)]
    logging.info(f"Created {len(chunks)} chunks for display")
    return chunks

async def send_no_history_message(interaction, page, user=None, ephemeral=True):
    if user:
        content = f"No chat history found for user {user.name} in this channel." if page == 1 else "No more history to display for this user."
    else:
        content = "This channel doesn't have any chat history yet." if page == 1 else "No more history to display."
    await interaction.followup.send(content, ephemeral=ephemeral)
    logging.info(f"No chat history found for channel {interaction.channel.id}, page {page}, user {user}")
