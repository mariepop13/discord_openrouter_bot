# Test Suite for Discord OpenRouter Bot

This directory contains unit tests for the main slash commands of the Discord OpenRouter Bot. These tests can be run independently of the main bot application.

## Test Files

- `test_ai_chat.py`: Tests for AI chat functionality
- `test_history_command.py`: Tests for history retrieval commands
- `test_general_commands.py`: Tests for general bot commands like ping and info
- `test_image_commands.py`: Tests for image generation and analysis commands
- `test_ai_preferences.py`: Tests for setting and getting AI preferences

## Running Tests

To run the tests, make sure you're in the project root directory and have all the required dependencies installed. Then, you can use the following command:

```
python -m unittest discover -v -s test
```

This command will discover and run all the tests in the `test` directory.

## Writing New Tests

When adding new features or commands to the bot, please add corresponding test cases to ensure the functionality works as expected. Follow the existing test structure and use mocking where appropriate to isolate the tested functionality.

Remember to run the test suite before submitting any pull requests to ensure your changes haven't broken existing functionality.
