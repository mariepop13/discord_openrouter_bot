import discord
from commands.general_commands import ping_command, help_command
from commands.ai_commands import ai_command, analyze_image_command

def setup_commands(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # Check if the bot is mentioned
        if bot.user.mentioned_in(message):
            await message.channel.send(f"Hello {message.author.mention}! How can I assist you?")
            return

        if message.content.startswith('!') or message.content.startswith('/'):
            command = message.content.split()[0].lower()
            args = message.content.split()[1:]

            if command in ['!ping', '/ping']:
                await ping_command(message)

            elif command in ['!help', '/help']:
                await help_command(message)

            elif command in ['!ai', '/ai']:
                await ai_command(message, args, bot)

            elif command in ['/analyse', '/analyze']:
                await analyze_image_command(message)

        # Messages without '!' or '/' prefix are ignored
