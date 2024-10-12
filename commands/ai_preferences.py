import discord
from utils.database import setup_database, set_personalization, set_ai_preferences

async def set_ai_preferences_command(interaction: discord.Interaction, option: str, value: str):
    conn, cursor = setup_database()  # This will ensure the database and tables are created
    
    try:
        if option in ['personality', 'tone', 'language', 'prebuild']:
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
