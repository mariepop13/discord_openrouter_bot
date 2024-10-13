# Discord OpenRouter Bot

This Discord bot uses OpenRouter.ai API to interact with various AI models, analyze images, and generate images using Replicate. The bot responds when mentioned and uses a set of commands for multiple functions.

## Setup

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Copy the `.env.template` file to create a new `.env` file:
   ```
   cp .env.template .env
   ```
4. Open the `.env` file and add the following:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   OPENROUTER_API_KEY=your_openrouter_api_key
   REPLICATE_API_TOKEN=your_replicate_api_token
   CLIENT_ID=your_discord_client_id
   ```
5. Replace `your_discord_bot_token`, `your_openrouter_api_key`, `your_replicate_api_token`, and `your_discord_client_id` with your actual tokens.

   Note: The `.env` file is crucial for the bot's operation. Make sure to keep it secure and never share it publicly.

## Running the Bot

To run the bot, execute the following command in the terminal:

```
python main.py
```

## Bot Behavior

The bot responds when it is mentioned (@bot_name) in a message or when specific commands are used. This ensures that the bot doesn't interfere with regular conversations unless explicitly called upon.

## Available Commands

### General Commands
- `/help`: Show the help message with all available commands
- `/ping`: Check if the bot is responsive
- `/clear`: Clear all conversation history

### AI Commands
- `/ai [message]`: Chat with the AI
- `/analyze [image]`: Analyze an attached image
- `/update_ai_settings`: Update AI settings (model, personality, tone, language, max tokens)

### Image Commands
- `/generate_image [prompt]`: Generate an image based on a prompt
- `/image_help`: Get help with image generation commands

## Usage Examples

- Chat with AI: `/ai Hello, how are you?`
- Analyze an image: `/analyze` (attach an image to your message)
- Generate an image: `/generate_image A beautiful sunset over the ocean`
- Update AI settings:
  - Set only the model: `/update_ai_settings model:gpt-openai/gpt-4o`
  - Set an option and value: `/update_ai_settings option:tone value:professional`
  - Set both model and an option: `/update_ai_settings model:openai/gpt-4o option:max_tokens value:2000`

## Contributing

Feel free to submit pull requests or create issues for any bugs or feature requests.

## License

This project is licensed under the MIT License.
