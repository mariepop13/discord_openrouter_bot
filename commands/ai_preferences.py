import discord
from utils.database import setup_database, set_personalization, set_ai_preferences

async def set_ai_option(interaction: discord.Interaction, option: str, value: str):
    conn, cursor = setup_database()  # This will ensure the database and tables are created
    
    try:
        if option in ['personality', 'tone', 'language']:
            set_personalization(cursor, interaction.user.id, option, value)
        elif option == 'model':
            set_ai_preferences(cursor, interaction.user.id, ai_model=value)
        elif option == 'max_tokens':
            try:
                max_tokens = int(value)
                set_ai_preferences(cursor, interaction.user.id, max_output=max_tokens)
            except ValueError:
                await interaction.response.send_message("Error: max_tokens must be an integer.")
                return
        else:
            await interaction.response.send_message(f"Invalid option: {option}")
            return
        
        conn.commit()
        await interaction.response.send_message(f"AI {option} set to: {value}")
    finally:
        conn.close()

async def set_ai_preferences_command(interaction: discord.Interaction, model: str = None, max_tokens: int = None):
    conn, cursor = setup_database()  # This will ensure the database and tables are created
    
    try:
        set_ai_preferences(cursor, interaction.user.id, ai_model=model, max_output=max_tokens)
        conn.commit()
        
        response = "AI preferences updated:"
        if model:
            response += f" Model set to {model}."
        if max_tokens:
            response += f" Max tokens set to {max_tokens}."
        
        await interaction.response.send_message(response)
    finally:
        conn.close()
