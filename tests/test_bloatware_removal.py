import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from src.bloatware_removal import ConnectionManager, PackageManager, CommandManager
import subprocess 


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
            text=True
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

class TestPackageManager:
    """Test cases for PackageManager class"""

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_success(self, mock_execute):
        """Test successful package retrieval"""
        mock_output = "package:com.example.app1\npackage:com.example.app2\npackage:com.system.app"
        mock_execute.return_value = mock_output

        packages = await PackageManager.get_installed_packages()
        
        expected_packages = ["com.example.app1", "com.example.app2", "com.system.app"]
        assert packages == expected_packages
        mock_execute.assert_called_once_with("adb shell pm list packages")

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_empty(self, mock_execute):
        """Test package retrieval with no packages"""
        mock_execute.return_value = ""

        packages = await PackageManager.get_installed_packages()
        
        assert packages == []

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_with_whitespace(self, mock_execute):
        """Test package retrieval with whitespace in output"""
        mock_output = "package:com.example.app1\n\npackage:com.example.app2\n  \n"
        mock_execute.return_value = mock_output

        packages = await PackageManager.get_installed_packages()
        
        expected_packages = ["com.example.app1", "com.example.app2"]
        assert packages == expected_packages

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_disable_success(self, mock_execute):
        """Test successful package disable operation"""
        mock_execute.return_value = "Success"

        action_form = {"action_com.example.app": "disable"}
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == []
        mock_execute.assert_called_once_with("adb shell pm disable-user --user 0 com.example.app")

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_uninstall_success(self, mock_execute):
        """Test successful package uninstall operation"""
        mock_execute.return_value = "Success"

        action_form = {"action_com.example.app": "uninstall"}
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == []
        mock_execute.assert_called_once_with("adb shell pm uninstall --user 0 com.example.app")

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_failure(self, mock_execute):
        """Test failed package operation"""
        mock_execute.return_value = "Failure: Package not found"

        action_form = {"action_com.example.app": "disable"}
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == ["com.example.app"]

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_no_action(self, mock_execute):
        """Test package operation with no action selected"""
        action_form = {"action_com.example.app": ""}
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == []
        mock_execute.assert_not_called()

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_multiple_actions(self, mock_execute):
        """Test multiple package operations"""
        mock_execute.side_effect = ["Success", "Failure", "Success"]

        action_form = {
            "action_com.example.app1": "disable",
            "action_com.example.app2": "uninstall",
            "action_com.example.app3": "disable"
        }
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == ["com.example.app2"]
        assert mock_execute.call_count == 3

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_invalid_action(self, mock_execute):
        """Test package operation with invalid action"""
        action_form = {"action_com.example.app": "invalid_action"}
        failed_packages = await PackageManager.perform_action_on_packages(action_form)
        
        assert failed_packages == ["com.example.app"]
        mock_execute.assert_called_once_with(":")


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

