import discord

def create_help_embed() -> discord.Embed:
    """Create the help command embed with all command information."""
    help_embed = discord.Embed(title="Discord OpenRouter Bot", color=discord.Color.blue())
    
    help_embed.description = (
        "This bot uses OpenRouter.ai API to interact with various AI models, "
        "analyze images, and generate images using Replicate. "
        "The bot responds when mentioned and uses the following commands:"
    )

    commands = {
        "General Commands": [
            ("/help", "Show this help message"),
            ("/ping", "Check if the bot is responsive"),
            ("/clear", "Clear all conversation history"),
            ("/purge [amount]", "Delete a specified number of messages (or all if no amount is given) - Admin only")
        ],
        "AI Commands": [
            ("/ai [message]", "Chat with the AI"),
            ("/analyze [image]", "Analyze an attached image"),
            ("/update_ai_settings", "Update AI settings (model, personality, tone, language, max tokens)")
        ],
        "Image Commands": [
            ("/generate_image [prompt]", "Generate an image based on a prompt"),
            ("/image_help", "Get help with image generation commands")
        ]
    }
    
    for category, command_list in commands.items():
        help_embed.add_field(
            name=category, 
            value="\n".join([f"`{cmd}`: {desc}" for cmd, desc in command_list]), 
            inline=False
        )
    
    help_embed.add_field(
        name="Usage Examples",
        value=(
            "• Chat with AI: `/ai Hello, how are you?`\n"
            "• Analyze an image: `/analyze` (attach an image to your message)\n"
            "• Generate an image: `/generate_image A beautiful sunset over the ocean`\n"
            "• Update AI settings: `/update_ai_settings model:openai/gpt-4o option:max_tokens value:2000`\n"
            "• Purge messages: `/purge 10` (deletes last 10 messages)"
        ),
        inline=False
    )
    
    return help_embed
