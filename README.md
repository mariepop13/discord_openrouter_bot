# Discord OpenRouter Bot

This Discord bot uses OpenRouter.ai API to interact with various AI models, analyze images, and generate images using Replicate. The bot now responds only when mentioned and uses a single /ai command for multiple functions.

## File Structure

- `main.py`: Entry point of the application
- `bot_setup.py`: Bot setup and configuration
- `commands.py`: Bot commands implementation
- `api_utils.py`: API-related functions
- `database.py`: Database operations
- `models.py`: Available AI models
- `requirements.txt`: List of required packages

## Setup

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add the following:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   OPENROUTER_API_KEY=your_openrouter_api_key
   REPLICATE_API_TOKEN=your_replicate_api_token
   ```
4. Replace `your_discord_bot_token`, `your_openrouter_api_key`, and `your_replicate_api_token` with your actual tokens.

## Running the Bot

To run the bot, execute the following command in the terminal:

```
python main.py
```

## Bot Behavior

The bot now only responds when it is mentioned (@bot_name) in a message. This ensures that the bot doesn't interfere with regular conversations unless explicitly called upon.

## Available Commands

- `/ai`: Main command for interacting with the AI. It has the following subcommands:
  - `chat`: Chat with the AI
  - `set_personality`: Set the AI's personality for chat
  - `set_tone`: Set the AI's tone for chat
  - `set_language`: Set the preferred language for AI chat
  - `generate_image`: Generate an image based on a prompt

  Usage examples:
  ```
  /ai action:chat message:"Hello, how are you?" model:openai/gpt-3.5-turbo max_tokens:100
  /ai action:set_personality personality:"friendly and helpful"
  /ai action:set_tone tone:"professional"
  /ai action:set_language language:"French"
  /ai action:generate_image message:"A beautiful sunset over the ocean"
  ```

- `/history`: Get your chat history
- `/models`: List available AI models

## Contributing

Feel free to submit pull requests or create issues for any bugs or feature requests.

## License

This project is licensed under the MIT License.
