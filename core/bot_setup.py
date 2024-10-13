import asyncio
from core.bot_initialization import initialize_bot
from core.command_registration import register_commands
from utils.database_schema import setup_database

def setup_bot():
    print("Setting up bot in bot_setup.py...")
    
    # Initialize the bot
    bot = initialize_bot()
    
    # Register slash commands
    register_commands(bot)
    
    # Setup the database
    asyncio.run(setup_database())
    
    print("Bot setup completed in bot_setup.py")
    return bot
