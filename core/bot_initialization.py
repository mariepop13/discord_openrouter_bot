import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from commands.ai_commands import ai_command

def initialize_bot():
    print("Initializing bot...")
    load_dotenv()
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        print(f"User ID: {bot.user.id}")
        print("Bot is ready!")

        # Generate and print invite link
        print("Generating invite link...")
        client_id = os.getenv('CLIENT_ID')
        if client_id:
            print(f"CLIENT_ID found: {client_id}")
            permissions = discord.Permissions.text()
            invite_link = discord.utils.oauth_url(client_id, permissions=permissions, scopes=("bot", "applications.commands"))
            print(f"\nBot invite link with required permissions:")
            print(invite_link)
        else:
            print("\nWarning: CLIENT_ID not found in .env file. Invite link couldn't be generated.")

        # Sync slash commands
        try:
            synced = await bot.tree.sync()
            print(f'Successfully synced {len(synced)} commands globally.')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    @bot.event
    async def on_message(message):
        if bot.user.mentioned_in(message) and not message.mention_everyone:
            # Create a mock interaction object
            class MockInteraction:
                def __init__(self, message):
                    self.message = message
                    self.user = message.author
                    self.client = bot

                async def response(self):
                    class MockResponse:
                        async def defer(self):
                            pass
                    return MockResponse()

                async def followup(self):
                    class MockFollowup:
                        async def send(self, content):
                            await message.channel.send(content)
                    return MockFollowup()

            mock_interaction = MockInteraction(message)
            await mock_interaction.response().defer()
            await ai_command(mock_interaction)
        await bot.process_commands(message)

    return bot
