from unittest.mock import AsyncMock, patch

import pytest

from src.device_manager import DeviceManager


@pytest.mark.asyncio
class TestDeviceManagerAsync:

    async def test_get_selected_device(self):
        result = await DeviceManager.get_selected_device()
        assert result == "test_device"

    async def test_set_selected_device(self):
        result = await DeviceManager.set_selected_device("serial456")
        assert result is True

    @patch("src.device_manager.DeviceManager.get_selected_device", new_callable=AsyncMock)
    @patch("src.device_manager.CommandManager.execute_command", new_callable=AsyncMock)
    async def test_list_devices_parses_output_and_marks_selected(
        self, mock_execute_command, mock_get_selected_device
    ):
        adb_output = (
            "List of devices attached\n"
            "serial123 device product:sdk_gphone_x86 model:Pixel_3a device:generic_x86\n"
            "serial456 device product:sdk_gphone_x86 model:Nexus_5 device:generic_x86\n"
            "serial789 unauthorized\n"
        )
        mock_execute_command.return_value = adb_output
        mock_get_selected_device.return_value = "serial456"

        devices = await DeviceManager.list_devices()
        assert isinstance(devices, list)
        assert len(devices) == 3

        # Check device fields
        for d in devices:
            assert "serial_number" in d
            assert "state" in d
            assert "model" in d
            assert "is_selected" in d

        # Check that the correct device is marked as selected
        selected = [d for d in devices if d["is_selected"]]
        assert len(selected) == 1
        assert selected[0]["serial_number"] == "serial456"

        # Check model parsing
        assert devices[0]["model"] == "Pixel_3a"
        assert devices[1]["model"] == "Nexus_5"
        assert devices[2]["model"] == "Unknown"  # No model in line

    @patch("src.device_manager.DeviceManager.get_selected_device", new_callable=AsyncMock)
    @patch("src.device_manager.CommandManager.execute_command", new_callable=AsyncMock)
    async def test_list_devices_empty_output(self, mock_execute_command, mock_get_selected_device):
        mock_execute_command.return_value = ""
        mock_get_selected_device.return_value = None
        devices = await DeviceManager.list_devices()
        assert devices == []

    @patch("src.device_manager.DeviceManager.get_selected_device", new_callable=AsyncMock)
    @patch("src.device_manager.CommandManager.execute_command", new_callable=AsyncMock)
    async def test_list_devices_no_devices(self, mock_execute_command, mock_get_selected_device):
        mock_execute_command.return_value = "List of devices attached\n"
        mock_get_selected_device.return_value = None
        devices = await DeviceManager.list_devices()
        assert devices == []
