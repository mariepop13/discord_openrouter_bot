import discord
from discord.ui import View, Button

class HistoryPaginationView(View):
    def __init__(self, user_id, channel_id, current_page, total_pages, filter_type, show_history_page_func):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.channel_id = channel_id
        self.current_page = current_page
        self.total_pages = total_pages
        self.filter_type = filter_type
        self.show_history_page = show_history_page_func

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 1:
            self.current_page -= 1
            await self.show_history_page(interaction, self.channel_id, self.current_page, self.filter_type, ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray, disabled=True)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.show_history_page(interaction, self.channel_id, self.current_page, self.filter_type, ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 1
        self.next_button.disabled = self.current_page == self.total_pages
