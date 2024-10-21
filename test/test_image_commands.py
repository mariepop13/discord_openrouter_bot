import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.commands.image_commands import generate_image_command, analyze_image_command

@pytest.mark.asyncio
@patch('src.commands.image_commands.analyze_image_impl')
async def test_analyze_image_command(mock_analyze_image_impl):
    interaction = AsyncMock()
    image = AsyncMock()
    mock_analyze_image_impl.return_value = "Image analysis result"

    await analyze_image_command(interaction, image)

    mock_analyze_image_impl.assert_called_once_with(interaction, image)

@pytest.mark.asyncio
@patch('src.commands.image_commands.generate_image')
@patch('src.commands.image_commands.get_timestamp_filename')
async def test_generate_image_command(mock_get_timestamp_filename, mock_generate_image):
    interaction = AsyncMock()
    prompt = "A beautiful sunset"
    model = "black-forest-labs/flux-dev"
    mock_generate_image.return_value = "http://example.com/image.jpg"
    mock_get_timestamp_filename.return_value = "2023-05-01_12-00-00.webp"

    await generate_image_command(interaction, prompt, model)

    mock_generate_image.assert_called_once_with(prompt, model, "generated_images/2023-05-01_12-00-00.webp")
    interaction.followup.send.assert_called()
