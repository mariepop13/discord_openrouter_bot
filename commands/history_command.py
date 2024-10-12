import discord
from discord import app_commands
from utils.database import get_history, setup_database
from datetime import datetime

@app_commands.command(name="history", description="View your chat history")
async def history(interaction: discord.Interaction, limit: int = 10):
    user_id = interaction.user.id
    
    conn, cursor = setup_database()
    try:
        chat_history = get_history(cursor, user_id, limit)
        
        if not chat_history:
            await interaction.response.send_message("You don't have any chat history yet.", ephemeral=True)
            return
        
        # Format the chat history
        formatted_history = []
        for content, model in chat_history:
            if model is None:
                formatted_history.append(f"**You**: {content}")
            else:
                formatted_history.append(f"**AI ({model})**: {content}")
        
        formatted_history = "\n\n".join(formatted_history[::-1])  # Reverse to show most recent last
        
        # Split the history into chunks if it's too long
        chunks = [formatted_history[i:i+4000] for i in range(0, len(formatted_history), 4000)]
        
        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"Your Chat History (Part {i+1}/{len(chunks)})",
                description=chunk,
                color=discord.Color.blue()
            )
            if i == len(chunks) - 1:
                embed.set_footer(text=f"Showing last {min(len(chat_history), limit)} messages")
            
            await interaction.followup.send(embed=embed, ephemeral=True) if i > 0 else await interaction.response.send_message(embed=embed, ephemeral=True)
    
    finally:
        conn.close()

async def setup(bot):
    bot.tree.add_command(history)
