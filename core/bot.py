import os
import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import aiohttp
from dotenv import load_dotenv
import replicate
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Database setup
conn = sqlite3.connect('bot_database.sqlite')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        model TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create comments table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create personalization table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS personalization (
        user_id INTEGER PRIMARY KEY,
        personality TEXT,
        tone TEXT,
        language TEXT
    )
''')
conn.commit()

# OpenRouter.ai API setup
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Available models
MODELS = [
    "google/gemini-flash-1.5",
    "openai/gpt-3.5-turbo",
    "openai/gpt-4",
    "anthropic/claude-2",
    "google/palm-2-chat-bison",
    "meta-llama/llama-2-70b-chat"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"User ID: {bot.user.id}")
    print("Bot is ready!")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await bot.process_commands(message)

@bot.tree.command(name="ai", description="Interact with the AI (chat, set personality, generate image, etc.)")
@app_commands.describe(
    action="The action to perform (chat, set_personality, set_tone, set_language, generate_image)",
    message="The message for chat or prompt for image generation",
    model="The AI model to use for chat (default: google/gemini-flash-1.5)",
    personality="The personality for the AI to adopt",
    tone="The tone for the AI to use",
    language="The language for the AI to use",
    max_tokens="Maximum number of tokens for the response (default: 150)"
)
@app_commands.choices(model=[
    app_commands.Choice(name=model.split('/')[-1], value=model)
    for model in MODELS
])
async def ai(
    interaction: discord.Interaction, 
    action: str,
    message: str = None,
    model: str = "google/gemini-flash-1.5",
    personality: str = None,
    tone: str = None,
    language: str = None,
    max_tokens: int = 150
):
    await interaction.response.defer()

    if action == "chat":
        # Get user personalization
        cursor.execute('SELECT personality, tone, language FROM personalization WHERE user_id = ?', (interaction.user.id,))
        personalization = cursor.fetchone()
        
        if personalization:
            pers, tn, lang = personalization
            message = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {message}"

        # Store the message in the database before the API call
        cursor.execute('INSERT INTO messages (user_id, content, model) VALUES (?, ?, ?)', (interaction.user.id, message, model))
        conn.commit()

        # Call OpenRouter.ai API
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    bot_response = result['choices'][0]['message']['content']
                    await interaction.followup.send(bot_response)
                else:
                    await interaction.followup.send("Sorry, I couldn't process your request.")

    elif action == "set_personality":
        if personality:
            cursor.execute('INSERT OR REPLACE INTO personalization (user_id, personality) VALUES (?, ?)', (interaction.user.id, personality))
            conn.commit()
            await interaction.followup.send(f"AI personality set to: {personality}")
        else:
            await interaction.followup.send("Please provide a personality.")

    elif action == "set_tone":
        if tone:
            cursor.execute('INSERT OR REPLACE INTO personalization (user_id, tone) VALUES (?, ?)', (interaction.user.id, tone))
            conn.commit()
            await interaction.followup.send(f"AI tone set to: {tone}")
        else:
            await interaction.followup.send("Please provide a tone.")

    elif action == "set_language":
        if language:
            cursor.execute('INSERT OR REPLACE INTO personalization (user_id, language) VALUES (?, ?)', (interaction.user.id, language))
            conn.commit()
            await interaction.followup.send(f"AI language set to: {language}")
        else:
            await interaction.followup.send("Please provide a language.")

    elif action == "generate_image":
        if message:
            try:
                output = replicate.run(
                    "black-forest-labs/flux-1.1-pro",
                    input={"prompt": message, "prompt_upsampling": True}
                )
                await interaction.followup.send(f"Generated image: {output}")
            except Exception as e:
                await interaction.followup.send(f"Sorry, I couldn't generate the image. Error: {str(e)}")
        else:
            await interaction.followup.send("Please provide a prompt for image generation.")

    else:
        await interaction.followup.send("Invalid action. Please use 'chat', 'set_personality', 'set_tone', 'set_language', or 'generate_image'.")

@bot.tree.command(name="history", description="Get your chat history")
@app_commands.describe(limit="Number of messages to retrieve (default: 5)")
async def history(interaction: discord.Interaction, limit: int = 5):
    cursor.execute('SELECT content, model FROM messages WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?', (interaction.user.id, limit))
    messages = cursor.fetchall()
    
    if messages:
        history = "\n".join([f"- [{msg[1]}] {msg[0]}" for msg in messages])
        await interaction.response.send_message(f"Your last {limit} messages:\n{history}")
    else:
        await interaction.response.send_message(f"You don't have any message history.")

@bot.tree.command(name="models", description="List available AI models")
async def list_models(interaction: discord.Interaction):
    model_list = "\n".join([f"- {model.split('/')[-1]}" for model in MODELS])
    await interaction.response.send_message(f"Available models:\n{model_list}")

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
