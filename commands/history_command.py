import discord
from discord import app_commands
from utils.database_operations import get_history
from datetime import datetime
import logging
import os
from discord.ui import View, Button

# These could be moved to a config file
MAX_MESSAGE_LENGTH = 500
MAX_EMBED_LENGTH = 4000
CLIENT_ID = int(os.getenv('CLIENT_ID', '0'))
MESSAGES_PER_PAGE = 5

def format_message(message_user_id, content, model, message_type, timestamp):
    formatted_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    icon = "🧑" if message_type == 'user' and message_user_id != CLIENT_ID else "🤖"
    sender = "You" if message_type == 'user' and message_user_id != CLIENT_ID else f"AI ({model})"
    
    formatted_message = f"{icon} **{sender}** - {formatted_time}\n```{content[:MAX_MESSAGE_LENGTH]}```"
    if len(content) > MAX_MESSAGE_LENGTH:
        formatted_message += "\n*(Message truncated)*"
    
    return formatted_message

class HistoryPaginationView(View):
    def __init__(self, user_id, current_page, total_pages):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.current_page = current_page
        self.total_pages = total_pages

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 1:
            self.current_page -= 1
            await show_history_page(interaction, self.user_id, self.current_page)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray, disabled=True)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.total_pages:
            self.current_page += 1
            await show_history_page(interaction, self.user_id, self.current_page)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 1
        self.next_button.disabled = self.current_page == self.total_pages

async def show_history_page(interaction: discord.Interaction, user_id: int, page: int = 1):
    try:
        offset = (page - 1) * MESSAGES_PER_PAGE
        chat_history = await get_history(user_id, MESSAGES_PER_PAGE, offset)
        
        if not chat_history:
            if page == 1:
                await interaction.response.send_message("You don't have any chat history yet.", ephemeral=True)
            else:
                await interaction.response.send_message("No more history to show.", ephemeral=True)
            return
        
        formatted_history = "\n\n".join([format_message(*message) for message in chat_history])
        chunks = [formatted_history[i:i+MAX_EMBED_LENGTH] for i in range(0, len(formatted_history), MAX_EMBED_LENGTH)]
        
        total_messages = await get_history(user_id, count_only=True)
        total_pages = (total_messages + MESSAGES_PER_PAGE - 1) // MESSAGES_PER_PAGE

        for i, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"Your Chat History (Page {page}/{total_pages})",
                description=chunk,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Showing messages {offset + 1}-{min(offset + MESSAGES_PER_PAGE, total_messages)} out of {total_messages}")
        
        view = HistoryPaginationView(user_id, page, total_pages)
        view.update_buttons()

        if interaction.response.is_done():
            await interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    except Exception as e:
        logging.error(f"Error in history command for user {user_id}: {str(e)}")
        await interaction.response.send_message("An error occurred while fetching your chat history. Please try again later.", ephemeral=True)

@app_commands.command(name="history", description="View your chat history")
async def history(interaction: discord.Interaction, page: int = 1):
    await interaction.response.defer(ephemeral=True)
    await show_history_page(interaction, interaction.user.id, page)

async def setup(bot):
    bot.tree.add_command(history)
