import pytest
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Run all test files
    pytest.main([
        "test/test_general_commands.py",
        "test/test_history_command.py",
        "test/test_ai_chat.py",
        "test/test_image_commands.py",
        "test/test_ai_preferences.py",
        "-v",
        "--disable-warnings"
    ])
