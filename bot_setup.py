import discord
from discord.ext import commands
from commands import setup_commands

def setup_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        print(f"User ID: {bot.user.id}")
        print("Bot is ready!")

        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if bot.user.mentioned_in(message):
            await bot.process_commands(message)

    setup_commands(bot)

    return bot
