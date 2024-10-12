import discord
from discord import app_commands
from utils.database import get_history
from datetime import datetime
import logging
import os

# These could be moved to a config file
MAX_MESSAGE_LENGTH = 500
MAX_EMBED_LENGTH = 4000
CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))

def format_message(user_id, content, model, message_type, timestamp):
    formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    icon = "🧑" if message_type == 'user' and user_id != CLIENT_ID else "🤖"
    sender = "You" if message_type == 'user' and user_id != CLIENT_ID else f"AI ({model})"
    
    formatted_message = f"{icon} **{sender}** - {formatted_time}\n```{content[:MAX_MESSAGE_LENGTH]}```"
    if len(content) > MAX_MESSAGE_LENGTH:
        formatted_message += "\n*(Message truncated)*"
    
    return formatted_message

@app_commands.command(name="history", description="View your chat history")
async def history(interaction: discord.Interaction, limit: int = 10):
    await interaction.response.defer(ephemeral=True)
    user_id = interaction.user.id
    
    try:
        chat_history = await get_history(user_id, limit)
        
        if not chat_history:
            await interaction.followup.send("You don't have any chat history yet.", ephemeral=True)
            return
        
        formatted_history = "\n\n".join([format_message(user_id, *message) for message in chat_history])
        chunks = [formatted_history[i:i+MAX_EMBED_LENGTH] for i in range(0, len(formatted_history), MAX_EMBED_LENGTH)]
        
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"Your Chat History (Part {i+1}/{len(chunks)})",
                description=chunk,
                color=discord.Color.blue()
            )
            if i == len(chunks) - 1:
                embed.set_footer(text=f"Showing last {min(len(chat_history), limit)} messages")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    except Exception as e:
        logging.error(f"Error in history command for user {user_id}: {str(e)}")
        await interaction.followup.send("An error occurred while fetching your chat history. Please try again later.", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(history)
