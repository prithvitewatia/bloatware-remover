import subprocess
from unittest.mock import MagicMock, patch

import pytest

from src.connection_manager import ConnectionManager


class TestConnectionManager:
    """Test cases for ConnectionManager class"""

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_connect_to_device_success(self, mock_popen):
        """Test successful device connection"""
        # Mock successful connection
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Success", "")
        mock_popen.return_value = mock_process

        result = await ConnectionManager.connect_to_device("192.168.1.100", "5555", "123456")

        assert result is True
        mock_popen.assert_called_once_with(
            ["adb", "pair", "192.168.1.100:5555"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_connect_to_device_failure(self, mock_popen):
        """Test failed device connection"""
        # Mock failed connection
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("failed to connect", "")
        mock_popen.return_value = mock_process

        result = await ConnectionManager.connect_to_device("192.168.1.100", "5555", "123456")

        assert result is False

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_connect_to_device_with_empty_code(self, mock_popen):
        """Test connection with empty pairing code"""
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Success", "")
        mock_popen.return_value = mock_process

        result = await ConnectionManager.connect_to_device("192.168.1.100", "5555", "")

        assert result is False
