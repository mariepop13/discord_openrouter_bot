import discord

async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())
    
    general_commands = [
        ("/help", "Show this help message"),
        ("/ping", "Check if the bot is responsive"),
        ("/clear", "Clear your command history")
    ]
    
    ai_commands = [
        ("/ai [message] (model) (max_output)", "Chat with the AI"),
        ("/set_ai_preferences (model) (max_output)", "Set AI preferences"),
        ("/analyze [image]", "Analyze an attached image")
    ]
    
    image_commands = [
        ("/generate_image [prompt]", "Generate an image based on a prompt"),
        ("/image_help", "Get help with image generation commands")
    ]
    
    embed.add_field(name="General Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in general_commands]), inline=False)
    embed.add_field(name="AI Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in ai_commands]), inline=False)
    embed.add_field(name="Image Commands", value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in image_commands]), inline=False)
    
    await interaction.response.send_message(embed=embed)
