import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.commands.general_commands import ping, help_command, clear, purge

@pytest.mark.asyncio
async def test_ping():
    interaction = AsyncMock()
    await ping(interaction)
    interaction.response.send_message.assert_called_once_with('Pong!', ephemeral=False)

@pytest.mark.asyncio
@patch('src.commands.help_content.discord.Embed')
async def test_help_command(mock_embed):
    interaction = AsyncMock()
    mock_embed_instance = mock_embed.return_value

    await help_command(interaction)

    mock_embed.assert_called_once()
    mock_embed_instance.add_field.assert_called()
    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
@patch('src.commands.general_commands.clear_command')
async def test_clear(mock_clear_command):
    interaction = AsyncMock()
    
    await clear(interaction)

    mock_clear_command.assert_called_once_with(interaction)

@pytest.mark.asyncio
async def test_purge():
    interaction = AsyncMock()
    interaction.channel = AsyncMock()
    deleted_messages = [AsyncMock() for _ in range(10)]
    interaction.channel.purge.return_value = deleted_messages

    await purge(interaction, 10)

    interaction.response.defer.assert_called_once_with(ephemeral=True)
    interaction.channel.purge.assert_called_once_with(limit=10)
    interaction.followup.send.assert_called_once_with("10 message(s) have been deleted.", ephemeral=True)
