import discord

def setup_commands(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Check if the bot is mentioned
        if bot.user.mentioned_in(message):
            await message.channel.send(f"Hello {message.author.mention}! How can I assist you? Use slash commands (/) to interact with me. For example, try /help to see available commands.")
            return

        # Process commands (required for both prefixed commands and slash commands to work)
        await bot.process_commands(message)
