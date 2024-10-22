import discord
from typing import List

async def get_channel_choices(interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
    choices = []
    for channel in interaction.guild.text_channels:
        if current.lower() in channel.name.lower():
            choices.append(discord.app_commands.Choice(name=channel.name, value=str(channel.id)))
    return choices[:25]  # Discord has a limit of 25 choices
