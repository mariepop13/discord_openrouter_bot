import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.commands.ai_chat import ai_command

@pytest.mark.asyncio
@patch('src.commands.ai_chat.chat_with_ai')
@patch('src.commands.ai_chat.get_ai_preferences')
@patch('src.commands.ai_chat.get_personalization')
@patch('src.commands.ai_chat.get_messages_for_channel')
@patch('src.commands.ai_chat.insert_message')
@patch('src.commands.ai_chat.is_interaction')
@patch('src.commands.ai_chat.send_message')
async def test_ai_command(mock_send_message, mock_is_interaction, mock_insert_message, mock_get_messages, mock_get_personalization, mock_get_ai_prefs, mock_chat_with_ai):
    interaction = AsyncMock()
    interaction.user.id = 123
    interaction.channel.id = 456
    
    # Mock the response and followup attributes
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    
    mock_is_interaction.return_value = True
    mock_get_ai_prefs.return_value = ('gpt-3.5-turbo', 150)
    mock_get_personalization.return_value = {}
    mock_get_messages.return_value = []
    mock_chat_with_ai.return_value = "AI response"

    await ai_command(interaction, "Hello, AI!")

    mock_get_ai_prefs.assert_called_once()
    mock_get_personalization.assert_called_once()
    mock_get_messages.assert_called_once()
    mock_chat_with_ai.assert_called_once()
    mock_insert_message.assert_called()
    interaction.response.defer.assert_called_once_with(thinking=True)
    mock_send_message.assert_called_once_with(interaction, "AI response")
