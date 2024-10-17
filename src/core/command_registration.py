import discord
from discord import app_commands
from src.commands.ai_preferences import update_ai_settings
from src.commands.image_commands import analyze_image_command, generate_image_command
from src.commands.general_commands import ping, help_command
from src.commands.history_command import history
from src.commands.ai_chat import ai_command
from src.database.history_operations import clear_channel_history, clear_user_history
from src.utils.history_utils import get_channel_choices
from typing import Optional, Literal, List
from src.utils.models import CHAT_MODELS, GENERATE_IMAGE_MODELS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIOption(discord.Enum):
    personality = "personality"
    tone = "tone"
    language = "language"
    prebuild = "prebuild"
    max_tokens = "max_tokens"
    custom = "custom"

def register_commands(bot):
    # AI and Chat Commands
    @bot.tree.command(name="ai", description="Chat with the AI")
    @app_commands.describe(message="Your message to the AI")
    async def ai_command_wrapper(interaction: discord.Interaction, message: str):
        logger.debug(f"Received /ai command with message: {message}")
        await ai_command(interaction, message)

    @bot.tree.command(name="update_ai_settings", description="Update AI settings")
    @app_commands.describe(
        option="The AI option to set (optional)",
        value="The value to set for the chosen option (optional)",
        model="The AI model to use",
        custom_option="If 'custom' is selected, specify the custom option here"
    )
    @app_commands.choices(model=[app_commands.Choice(name=model, value=model) for model in CHAT_MODELS])
    async def update_ai_settings_wrapper(
        interaction: discord.Interaction, 
        model: Optional[str] = None,
        option: Optional[AIOption] = None,
        value: Optional[str] = None,
        custom_option: Optional[str] = None
    ):
        option_value = custom_option if option == AIOption.custom else option.value if option else None
        logger.debug(f"Received /update_ai_settings command with model: {model}, option: {option}, value: {value}, custom_option: {custom_option}")
        await update_ai_settings(interaction, option_value, value, model)

    # Image Commands
    @bot.tree.command(name="analyze", description="Analyze an attached image")
    @app_commands.describe(image="The image to analyze")
    async def analyze(interaction: discord.Interaction, image: discord.Attachment):
        logger.debug(f"Received /analyze command with image: {image.filename}")
        if not image.content_type.startswith('image/'):
            await interaction.response.send_message("The uploaded file is not an image. Please upload an image file.")
            return
        await interaction.response.defer()
        await analyze_image_command(interaction, image)

    @bot.tree.command(name="generate_image", description="Generate an image based on a prompt")
    @app_commands.describe(
        prompt="Your image generation prompt",
        model="The image generation model to use"
    )
    @app_commands.choices(model=[app_commands.Choice(name=model, value=model) for model in GENERATE_IMAGE_MODELS])
    async def generate_image(interaction: discord.Interaction, prompt: str, model: str = "black-forest-labs/flux-dev"):
        logger.debug(f"Received /generate_image command with prompt: {prompt}, model: {model}")
        await interaction.response.defer()
        await generate_image_command(interaction, prompt, model, bot)

    # Clear Command
    @bot.tree.command(name="clear", description="Clear messages from a channel")
    @app_commands.describe(
        target="Choose where to clear messages from",
        channel="The channel to clear messages from (if 'other' is selected)"
    )
    async def clear_command(
        interaction: discord.Interaction,
        target: Literal["current", "other", "all"],
        channel: Optional[str] = None
    ):
        logger.debug(f"Received /clear command with target: {target}, channel: {channel}")
        
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("You don't have permission to clear messages.", ephemeral=True)
            return

        try:
            if target == "current":
                deleted = await clear_channel_history(interaction.channel.id)
                await interaction.response.send_message(f"Cleared {deleted} messages from the current channel.", ephemeral=True)
            elif target == "other":
                if channel is None:
                    await interaction.response.send_message("You must specify a channel when selecting 'other'.", ephemeral=True)
                    return
                channel_id = int(channel)
                target_channel = interaction.guild.get_channel(channel_id)
                if target_channel is None:
                    await interaction.response.send_message("Invalid channel selected.", ephemeral=True)
                    return
                deleted = await clear_channel_history(channel_id)
                await interaction.response.send_message(f"Cleared {deleted} messages from {target_channel.mention}.", ephemeral=True)
            elif target == "all":
                deleted = await clear_user_history()
                await interaction.response.send_message(f"Cleared {deleted} messages and comments from all channels.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages in that channel.", ephemeral=True)
        except Exception as e:
            logger.error(f"Error in clear command: {str(e)}")
            await interaction.response.send_message(f"An error occurred while clearing messages: {str(e)}", ephemeral=True)

    @clear_command.autocomplete("channel")
    async def clear_channel_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        return await get_channel_choices(interaction, current)

    # Utility Commands
    @bot.tree.command(name="help", description="Get information about available commands")
    async def help_command_wrapper(interaction: discord.Interaction):
        logger.debug("Received /help command")
        await help_command(interaction)

    @bot.tree.command(name="ping", description="Check if the bot is responsive")
    async def ping_command(interaction: discord.Interaction):
        logger.debug("Received /ping command")
        await ping(interaction)

    @bot.tree.command(name="models", description="List available AI models")
    async def list_models(interaction: discord.Interaction):
        model_list = "\n".join([f"- {model.split('/')[-1]}" for model in CHAT_MODELS])
        await interaction.response.send_message(f"Available models:\n{model_list}")
        logger.debug("Listed available models.")

    # Register the history command
    bot.tree.add_command(history)

    logger.info("All commands registered successfully.")
