import discord
from utils.api_utils import chat_with_ai, generate_image, analyze_image
from utils.database import insert_message, get_personalization, set_personalization

async def analyze_image_command(message):
    if len(message.attachments) == 0:
        await message.channel.send("Please upload an image with the /analyse command.")
        return

    image = message.attachments[0]
    if not image.content_type.startswith('image/'):
        await message.channel.send("The uploaded file is not an image. Please upload an image file.")
        return

    try:
        image_url = image.url
        description = await analyze_image(image_url)
        await message.channel.send(f"Image analysis: {description}")
    except Exception as e:
        await message.channel.send(f"Sorry, I couldn't analyze the image. Error: {str(e)}")

async def ai_command(message, args, bot):
    if len(args) < 1:
        await message.channel.send("Usage: !ai [action] [message]")
        return

    action = args[0]
    msg = ' '.join(args[1:]) if len(args) > 1 else ""

    if action == "chat":
        personalization = get_personalization(bot.db_cursor, message.author.id)
        
        if personalization:
            pers, tn, lang = personalization
            msg = f"Please respond as if you have a {pers} personality, with a {tn} tone, in {lang} language. User message: {msg}"

        insert_message(bot.db_cursor, message.author.id, msg, "google/gemini-flash-1.5")
        bot.db_conn.commit()

        bot_response = await chat_with_ai("google/gemini-flash-1.5", msg, 150)
        await message.channel.send(bot_response)

    elif action in ["set_personality", "set_tone", "set_language"]:
        if msg:
            set_personalization(bot.db_cursor, message.author.id, action.split('_')[1], msg)
            bot.db_conn.commit()
            await message.channel.send(f"AI {action.split('_')[1]} set to: {msg}")
        else:
            await message.channel.send(f"Please provide a {action.split('_')[1]}.")

    elif action == "generate_image":
        if msg:
            try:
                output = await generate_image(msg)
                await message.channel.send(f"Generated image: {output}")
            except Exception as e:
                await message.channel.send(f"Sorry, I couldn't generate the image. Error: {str(e)}")
        else:
            await message.channel.send("Please provide a prompt for image generation.")

    elif action == "analyse":
        await analyze_image_command(message)

    else:
        await message.channel.send("Invalid action. Please use 'chat', 'set_personality', 'set_tone', 'set_language', 'generate_image', or 'analyse'.")
