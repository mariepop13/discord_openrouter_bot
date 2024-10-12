import discord

async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    
    general_commands = [
        ("/help", "Show this help message with all available commands"),
        ("/ping", "Check if the bot is responsive and get its latency"),
        ("/clear", "Clear your command history from the bot's database"),
        ("/history (limit)", "View your recent chat history, optionally specify the number of messages to show")
    ]
    
    ai_commands = [
        ("/ai [message] (model) (max_output)", "Chat with the AI, optionally specifying the model and maximum output length"),
        ("/set_ai_preferences (model) (max_output)", "Set your default AI model and maximum output length"),
        ("/analyze [image]", "Analyze an attached image using AI")
    ]
    
    image_commands = [
        ("/generate_image [prompt]", "Generate an image based on a text prompt using AI"),
        ("/image_help", "Get detailed help with image generation commands and options")
    ]
    
    embed.add_field(name="General Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in general_commands]), inline=False)
    embed.add_field(name="AI Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in ai_commands]), inline=False)
    embed.add_field(name="Image Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in image_commands]), inline=False)
    
    await interaction.response.send_message(embed=embed)
