# Discord OpenRouter Bot

Version: 0.1.0-alpha

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
4. Open the `.env` file and replace the placeholder values with your actual credentials and settings.

   Explanation of each variable in the `.env` file:

   - `DISCORD_TOKEN`: The authentication token for your Discord bot.
   - `OPENROUTER_API_KEY`: Your API key to access OpenRouter services.
   - `REPLICATE_API_TOKEN`: Your API token to use Replicate services (for image generation).
   - `CLIENT_ID`: The client ID of your Discord application.
   - `LOG_FILES_TO_KEEP`: The number of log files to keep before rotation.
   - `BOT_NAME`: The name of your Discord bot.
   - `IMAGE_ANALYSIS_MODEL`: Configuration for the image analysis model (defaults to OpenAI chatgpt-4o).
   - `CHAT_MODEL`: Configuration for the chat model (defaults to Google Gemini Flash 1.5).
   - `HISTORY_LIMIT`: The maximum number of messages to keep in the conversation history.

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
- `/history [channel] [page] [filter_type] [user]`: View chat history (admin-only for user parameter)
  - `channel`: Optional. The channel to view history for.
  - `page`: Optional. The page number to view (default: 1).
  - `filter_type`: Optional. Filter type: 'all', 'chat', or 'image' (default: all).
  - `user`: Optional, admin-only. The user to view history for.

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
- View chat history:
  - View history for current channel: `/history`
  - View history for a specific channel: `/history channel:#general`
  - View history with pagination: `/history page:2`
  - View history with filter: `/history filter_type:chat`
  - Admin view history for a specific user: `/history user:@username`

## Contributing

Feel free to submit pull requests or create issues for any bugs or feature requests.

## License

This project is licensed under the MIT License.
