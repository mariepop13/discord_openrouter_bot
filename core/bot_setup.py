from core.bot_initialization import initialize_bot
from core.command_registration import register_commands

def setup_bot():
    print("Setting up bot in bot_setup.py...")
    
    # Initialize the bot
    bot = initialize_bot()
    
    # Register slash commands
    register_commands(bot)
    
    print("Bot setup completed in bot_setup.py")
    return bot
