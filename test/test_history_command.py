import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.commands.history_command import register_history_command

class MockCommand:
    def __init__(self):
        self.callback = None
        self.autocomplete = MagicMock()

    def __call__(self, func):
        self.callback = func
        return self

@pytest.mark.asyncio
@patch('src.commands.history_command.show_history_page')
async def test_history_command(mock_show_history_page):
    bot = MagicMock()
    mock_command = MockCommand()
    bot.tree.command = MagicMock(return_value=mock_command)
    
    register_history_command(bot)
    
    # Check if bot.tree.command was called
    bot.tree.command.assert_called_once()
    
    # Get the arguments passed to bot.tree.command
    command_args = bot.tree.command.call_args[1]
    assert command_args['name'] == "history"
    assert "View your chat history" in command_args['description']
    
    # Ensure the callback was set
    assert mock_command.callback is not None
    
    # Simulate calling the command
    interaction = AsyncMock()
    interaction.user = AsyncMock()
    interaction.user.guild_permissions.administrator = True
    interaction.guild.get_channel.return_value = AsyncMock()
    
    await mock_command.callback(interaction, channel=None, page=1, filter_type='all', user=None)
    
    interaction.response.defer.assert_called_once_with(ephemeral=True)
    mock_show_history_page.assert_called_once()

    # Check if autocomplete was set
    assert hasattr(mock_command, 'autocomplete')
    assert mock_command.autocomplete.called
