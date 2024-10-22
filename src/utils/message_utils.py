import discord
from discord import Interaction
import logging
from typing import Optional, List, Dict, Tuple, Union

logger = logging.getLogger(__name__)

async def send_message(
    interaction: Interaction, 
    content: str, 
    ephemeral: bool = True, 
    embed: Optional[discord.Embed] = None
):
    """Send a message through a Discord interaction with optional embed."""
    try:
        if embed:
            await interaction.response.send_message(
                content=content, 
                embed=embed, 
                ephemeral=ephemeral
            )
        else:
            await interaction.response.send_message(content, ephemeral=ephemeral)
        logger.debug(f"Message sent: {content}")
    except discord.errors.NotFound:
        if embed:
            await interaction.followup.send(
                content=content, 
                embed=embed, 
                ephemeral=ephemeral
            )
        else:
            await interaction.followup.send(content, ephemeral=ephemeral)
        logger.debug(f"Follow-up message sent: {content}")

def get_personalized_message(personalization: Dict[str, str], message: str) -> str:
    """
    Apply user personalization settings to the message.
    
    Args:
        personalization: Dictionary containing personalization settings
        message: Original message to personalize
    
    Returns:
        Personalized message string
    """
    if not personalization:
        return message

    personality = personalization.get('personality', '')
    tone = personalization.get('tone', '')
    language = personalization.get('language', '')

    system_prompt = []
    if personality:
        system_prompt.append(f"Personality: {personality}")
    if tone:
        system_prompt.append(f"Tone: {tone}")
    if language:
        system_prompt.append(f"Language: {language}")

    if system_prompt:
        return f"{' | '.join(system_prompt)}\n\nUser message: {message}"
    return message

def format_chat_history(chat_history: List[Tuple]) -> List[Dict[str, str]]:
    """
    Format chat history into a list of message dictionaries suitable for AI processing.
    
    Args:
        chat_history: List of tuples from the database containing
                     (user_id, content, model, message_type, timestamp, mentioned_user_id)
    
    Returns:
        List of formatted message dictionaries with role and content
    """
    formatted_messages = []
    for msg in chat_history:
        # msg[3] is message_type from the tuple
        role = "assistant" if msg[3] == 'bot' else "user"
        # msg[1] is content from the tuple
        formatted_messages.append({
            "role": role,
            "content": msg[1]
        })
    return formatted_messages
