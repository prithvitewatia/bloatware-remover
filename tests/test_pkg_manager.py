from unittest.mock import patch

import pytest

from src.cmd_manager import CommandManager
from src.exceptions import ErrorCodes
from src.pkg_manager import PackageManager


class TestPackageManager:
    """Test cases for PackageManager class"""

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_success(self, mock_execute):
        """Test successful package retrieval"""
        mock_output = "package:com.example.app1\npackage:com.example.app2\npackage:com.system.app"
        mock_execute.return_value = mock_output

        return_code, packages = await PackageManager.get_installed_packages()

        expected_packages = ["com.example.app1", "com.example.app2", "com.system.app"]
        assert packages == expected_packages
        assert return_code == ErrorCodes.SUCCESS
        mock_execute.assert_called_once_with("adb -s test_device shell pm list packages")

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_empty(self, mock_execute):
        """Test package retrieval with no packages"""
        mock_execute.return_value = ""

        return_code, packages = await PackageManager.get_installed_packages()

        assert packages == []
        assert return_code == ErrorCodes.NO_PACKAGES_FOUND

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_get_installed_packages_with_whitespace(self, mock_execute):
        """Test package retrieval with whitespace in output"""
        mock_output = "package:com.example.app1\n\npackage:com.example.app2\n  \n"
        mock_execute.return_value = mock_output

        return_code, packages = await PackageManager.get_installed_packages()

        expected_packages = ["com.example.app1", "com.example.app2"]
        assert packages == expected_packages
        assert return_code == ErrorCodes.SUCCESS

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_disable_success(self, mock_execute):
        """Test successful package disable operation"""
        mock_execute.return_value = "Success"

        action_form = {"action_com.example.app": "disable"}
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == []
        assert return_code == ErrorCodes.SUCCESS
        mock_execute.assert_called_once_with(
            "adb -s test_device shell pm disable-user --user 0 com.example.app"
        )

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_uninstall_success(self, mock_execute):
        """Test successful package uninstall operation"""
        mock_execute.return_value = "Success"

        action_form = {"action_com.example.app": "uninstall"}
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == []
        assert return_code == ErrorCodes.SUCCESS
        mock_execute.assert_called_once_with(
            "adb -s test_device shell pm uninstall --user 0 com.example.app"
        )

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_failure(self, mock_execute):
        """Test failed package operation"""
        mock_execute.return_value = "Failure: Package not found"

        action_form = {"action_com.example.app": "disable"}
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == ["com.example.app"]
        assert return_code == ErrorCodes.FAILED_OPERATION

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_no_action(self, mock_execute):
        """Test package operation with no action selected"""
        action_form = {"action_com.example.app": ""}
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == []
        assert return_code == ErrorCodes.SUCCESS
        mock_execute.assert_not_called()

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_multiple_actions(self, mock_execute):
        """Test multiple package operations"""
        mock_execute.side_effect = ["Success", "Failure", "Success"]

        action_form = {
            "action_com.example.app1": "disable",
            "action_com.example.app2": "uninstall",
            "action_com.example.app3": "disable",
        }
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == ["com.example.app2"]
        assert return_code == ErrorCodes.FAILED_OPERATION
        assert mock_execute.call_count == 3

    @pytest.mark.asyncio
    @patch.object(CommandManager, 'execute_command')
    async def test_perform_action_on_packages_invalid_action(self, mock_execute):
        """Test package operation with invalid action"""
        action_form = {"action_com.example.app": "invalid_action"}
        return_code, failed_packages = await PackageManager.perform_action_on_packages(action_form)

        assert failed_packages == ["com.example.app"]
        assert return_code == ErrorCodes.FAILED_OPERATION
        mock_execute.assert_called_once_with(":")
