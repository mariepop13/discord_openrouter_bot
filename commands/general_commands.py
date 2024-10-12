async def ping_command(message):
    await message.channel.send('Pong!')

async def help_command(message):
    commands = [
        "!ai or /ai [action] [message] - Interact with the AI (chat, set personality, generate image, etc.)",
        "!ping or /ping - Check if the bot is responsive",
        "!help or /help - List all available commands",
        "!analyze or /analyze - Analyze an uploaded image (upload an image with this command)"
    ]
    command_list = "\n".join(commands)
    await message.channel.send(f"Available commands:\n{command_list}")
