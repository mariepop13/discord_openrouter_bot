import discord
from utils.database import clear_user_history

async def ping(interaction: discord.Interaction):
    await interaction.followup.send('Pong!')

async def help_command(interaction: discord.Interaction):
    commands = [
        "/ai [message] - Chat with the AI",
        "/analyze [image] - Analyze an attached image",
        "/clear - Clear your command history",
        "/generate_image [prompt] - Generate an image based on a prompt",
        "/help - Show this help message",
        "/image_help - Get help with image generation commands",
        "/ping - Check if the bot is responsive"
    ]
    command_list = "\n".join(commands)
    await interaction.followup.send(f"Available commands:\n{command_list}")

async def clear(interaction: discord.Interaction):
    allowed_user_id = 451176341740716042  # Replace this with the actual allowed user ID
    if interaction.user.id != allowed_user_id:
        await interaction.followup.send("Sorry, you are not authorized to use this command.", ephemeral=True)
        return

    bot = interaction.client
    rows_deleted = clear_user_history(bot.db_cursor, interaction.user.id)
    bot.db_conn.commit()

    await interaction.followup.send(f"Your command history has been cleared. {rows_deleted} entries have been deleted.", ephemeral=True)
