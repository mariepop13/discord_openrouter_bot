import discord
import logging
from typing import Union

async def send_message(ctx: Union[discord.Interaction, discord.Message], message: str):
    try:
        if isinstance(ctx, discord.Interaction):
            if ctx.response.is_done():
                await ctx.followup.send(message)
            else:
                await ctx.response.send_message(message)
        else:
            await ctx.channel.send(message)
        logging.debug(f"Sent message: {message}")
    except Exception as e:
        logging.error(f"Failed to send message: {str(e)}", exc_info=True)

def get_user_id(ctx: Union[discord.Interaction, discord.Message]) -> int:
    return ctx.author.id if hasattr(ctx, 'author') else ctx.user.id

def get_channel_id(ctx: Union[discord.Interaction, discord.Message]) -> int:
    return ctx.channel.id

def is_interaction(ctx: Union[discord.Interaction, discord.Message]) -> bool:
    return isinstance(ctx, discord.Interaction)
