import logging
import subprocess


class ConnectionManager:
    logger = logging.getLogger(__name__)

    @classmethod
    async def connect_to_device(cls, device_ip, device_port, device_code) -> bool:
        """
        Connect to a device using ADB pairing.
        This method uses the ADB command to pair with a device using its IP address and port.
        It requires the device to be in pairing mode and the user to provide a six-digit pairing code.
        :param device_ip: Device IP address.
        :param device_port: Device port number.
        :param device_code: Device pairing code (six-digit).
        :return: True if the connection was successful, False otherwise.
        """

        if not (device_ip and device_port and device_code):
            return False
        cls.logger.debug(f"Connecting to device {device_ip}:{device_port}...")
        process = subprocess.Popen(
            ["adb", "pair", f"{device_ip}:{device_port}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = process.communicate(input=device_code + "\n")
        status = 'failed' not in stdout
        cls.logger.debug(f"Connection status for device {device_ip}:{device_port}:{status}.")
        return status
