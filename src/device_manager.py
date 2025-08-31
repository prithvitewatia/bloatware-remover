import logging
import re

from src.cmd_manager import CommandManager
from src.db import db_manager


class DeviceManager:
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_selected_device(cls):
        """Get the currently selected device from the database as a str"""
        return await db_manager.get_selected_device()

    @classmethod
    async def set_selected_device(cls, serial_number):
        """Set the currently selected device in the database."""
        await db_manager.set_selected_device(serial_number)
        return True

    @classmethod
    async def list_devices(cls):
        """
        List connected devices using ADB.
        Returns a list of connected devices with their following details.
        Serial Number, State, Description
        Returns a list of online devices only ie. state = device.
        """
        cmd = "adb devices -l"
        output = await CommandManager.execute_command(cmd)
        devices = []
        if output:
            regex = r"^(\S+)\s+(\S+)(?:\s+.*model:(\S+))?"
            # Skip the first line as it is a header
            lines = output.strip().split("\n")[1:]
            for line in lines:
                match = re.match(regex, line)
                if match:
                    serial_number, state, model = match.groups()
                    devices.append(
                        {
                            "serial_number": serial_number,
                            "state": state,
                            "model": model if model else "Unknown",
                            "is_selected": False,
                        }
                    )
        current_device = await cls.get_selected_device()
        if current_device:
            for device in devices:
                if device["serial_number"] == current_device:
                    device["is_selected"] = True

        return devices
