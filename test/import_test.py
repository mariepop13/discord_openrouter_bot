import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    from src.commands.general_commands import ping, help_command, clear, purge
    print("Successfully imported ping, help_command, clear, and purge from general_commands")
except ImportError as e:
    print(f"Failed to import from general_commands: {e}")

try:
    import unittest
    print("Successfully imported unittest")
except ImportError as e:
    print(f"Failed to import unittest: {e}")

try:
    from unittest.mock import MagicMock, patch
    print("Successfully imported MagicMock and patch")
except ImportError as e:
    print(f"Failed to import MagicMock or patch: {e}")
