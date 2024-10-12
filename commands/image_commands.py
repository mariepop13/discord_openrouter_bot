import discord
import asyncio
from utils.api_utils import generate_image

async def generate_image_command(interaction: discord.Interaction, prompt: str, bot):
    await interaction.followup.send("Generating image... This may take a few minutes.")

    try:
        output = await generate_image(prompt)
        if output:
            await interaction.followup.send(f"Generated image: {output}")
        else:
            await interaction.followup.send("Sorry, I couldn't generate the image. Please try again with a different prompt.")
    except Exception as e:
        await interaction.followup.send(f"Sorry, an error occurred while generating the image: {str(e)}")

async def image_generation_help(interaction: discord.Interaction):
    help_text = """
    Image Generation Command Help:
    
    Usage: /generate_image <prompt>
    
    Options:
    - prompt: Your description of the image you want to generate.
    
    Example:
    /generate_image A beautiful sunset over the ocean
    
    Note: Image generation may take a few minutes. Please be patient.
    """
    await interaction.followup.send(help_text)

async def analyze_image_command(interaction: discord.Interaction, image: discord.Attachment):
    # This function is already implemented in ai_commands.py
    # We're keeping it here for consistency, but you may want to move it to this file in the future
    from commands.ai_commands import analyze_image_command as analyze_image_impl
    await analyze_image_impl(interaction, image)
