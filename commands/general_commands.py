import discord
from utils.database import clear_user_history

async def ping(interaction: discord.Interaction):
    await interaction.followup.send('Pong!')

async def help_command(interaction: discord.Interaction):
    help_embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    
    general_commands = [
        ("/help", "Show this help message"),
        ("/ping", "Check if the bot is responsive"),
        ("/clear", "Clear your command history (Authorized users only)")
    ]
    
    ai_commands = [
        ("/ai [message]", "Chat with the AI"),
        ("/analyze [image]", "Analyze an attached image")
    ]
    
    image_commands = [
        ("/generate_image [prompt]", "Generate an image based on a prompt"),
        ("/image_help", "Get help with image generation commands")
    ]
    
    help_embed.add_field(name="General Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in general_commands]), inline=False)
    help_embed.add_field(name="AI Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in ai_commands]), inline=False)
    help_embed.add_field(name="Image Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in image_commands]), inline=False)
    
    await interaction.followup.send(embed=help_embed)

async def clear(interaction: discord.Interaction):
    allowed_user_id = 451176341740716042  # Replace this with the actual allowed user ID
    if interaction.user.id != allowed_user_id:
        await interaction.followup.send("Sorry, you are not authorized to use this command.", ephemeral=True)
        return

    bot = interaction.client
    rows_deleted = clear_user_history(bot.db_cursor, interaction.user.id)
    bot.db_conn.commit()

    await interaction.followup.send(f"Your command history has been cleared. {rows_deleted} entries have been deleted.", ephemeral=True)
