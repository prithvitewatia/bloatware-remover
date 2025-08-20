import subprocess
from unittest.mock import MagicMock, patch

import pytest

from src.cmd_manager import CommandManager


class TestCommandManager:
    """Test cases for CommandManager class"""

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_execute_command_success(self, mock_popen):
        """Test successful command execution"""
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Command output", "")
        mock_popen.return_value = mock_process

        result = await CommandManager.execute_command("adb devices")

        assert result == "Command output"
        mock_popen.assert_called_once_with(
            "adb devices",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_execute_command_exception(self, mock_popen):
        """Test command execution with exception"""
        mock_popen.side_effect = Exception("Command failed")

        result = await CommandManager.execute_command("invalid_command")

        assert result == ""

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_execute_command_with_stderr(self, mock_popen):
        """Test command execution with stderr output"""
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Command output", "Error message")
        mock_popen.return_value = mock_process

        result = await CommandManager.execute_command("adb devices")

        assert result == "Command output"
