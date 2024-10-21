import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.commands.ai_preferences import update_ai_settings, PERSONALITY, MAX_TOKENS

@pytest.mark.asyncio
@patch('src.commands.ai_preferences.set_ai_preferences')
@patch('src.commands.ai_preferences.set_personalization')
@patch('src.commands.ai_preferences.CHAT_MODELS', ['gpt-3.5-turbo', 'gpt-4'])
async def test_update_ai_settings(mock_set_personalization, mock_set_ai_preferences):
    interaction = AsyncMock()
    interaction.user.id = 123

    # Test updating the model
    await update_ai_settings(interaction, model="gpt-3.5-turbo")
    mock_set_ai_preferences.assert_called_once_with(123, ai_model="gpt-3.5-turbo")
    interaction.response.send_message.assert_called_once_with("AI model set to: gpt-3.5-turbo", ephemeral=True)

    # Reset mocks
    mock_set_ai_preferences.reset_mock()
    interaction.response.send_message.reset_mock()

    # Test updating personality
    await update_ai_settings(interaction, option=PERSONALITY, value="friendly")
    mock_set_personalization.assert_called_once_with(123, PERSONALITY, "friendly")
    interaction.response.send_message.assert_called_once_with("AI personality set to: friendly", ephemeral=True)

    # Reset mocks
    mock_set_personalization.reset_mock()
    interaction.response.send_message.reset_mock()

    # Test updating max_tokens
    await update_ai_settings(interaction, option=MAX_TOKENS, value="2000")
    mock_set_ai_preferences.assert_called_once_with(123, max_output=2000)
    interaction.response.send_message.assert_called_once_with("AI max tokens set to: 2000", ephemeral=True)

    # Reset mocks
    mock_set_ai_preferences.reset_mock()
    interaction.response.send_message.reset_mock()

    # Test invalid option
    await update_ai_settings(interaction, option="invalid_option", value="some_value")
    mock_set_ai_preferences.assert_not_called()
    mock_set_personalization.assert_not_called()
    interaction.response.send_message.assert_called_once_with("Invalid option: invalid_option", ephemeral=True)

    # Reset mocks
    interaction.response.send_message.reset_mock()

    # Test invalid model
    await update_ai_settings(interaction, model="invalid-model")
    mock_set_ai_preferences.assert_not_called()
    interaction.response.send_message.assert_called_once_with("Error: Invalid model selection.", ephemeral=True)
