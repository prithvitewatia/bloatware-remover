import logging
import subprocess



class PackageManager:

    logger = logging.getLogger(__name__)

    @classmethod
    async def get_installed_packages(cls)->list[str]:
        """
        Get a list of installed packages on the device.
        :return: A list of installed packages that match the filter.
        """
        cmd = "adb shell pm list packages"
        stdout = await CommandManager.execute_command(cmd)
        if not stdout:
            cls.logger.warning(f"No packages found")
            return []

        return [
            package.strip().replace("package:", "",1)
            for package in stdout.split("\n") if package.strip()
        ]

    @classmethod
    async def perform_action_on_packages(cls, action_form):
        """
        Perform actions on packages based on the provided operation map.
        :param action_form: A dictionary containing the action to perform on each package.
        :return: A list of packages on which operation was not successful.
        """
        failed_operations = []
        for key, value in action_form.items():
            if key.startswith("action_") and value:  # skip "no action"
                pkg = key.replace("action_", "")
                cls.logger.info(f"Performing action {value} on {pkg}")
                if value == "disable":
                    cmd = f"adb shell pm disable-user --user 0 {pkg}"
                elif value == "uninstall":
                    cmd = f"adb shell pm uninstall --user 0 {pkg}"
                else:
                    cmd = ":"  # No op command just to keep the structure
                stdout = await CommandManager.execute_command(cmd)
                cls.logger.debug(f"stdout: {stdout} for {pkg}")
                if 'Success' not in stdout:
                    failed_operations.append(pkg)
        return failed_operations

class ConnectionManager:
    logger = logging.getLogger(__name__)

    @classmethod
    async def connect_to_device(cls, device_ip, device_port, device_code)->bool:
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
            text=True
        )
        stdout, stderr = process.communicate(input=device_code + "\n")
        status = 'failed' not in stdout
        cls.logger.debug(f"Connection status for device {device_ip}:{device_port}:{status}.")
        return status

class CommandManager:
    logger = logging.getLogger(__name__)

    @classmethod
    async def execute_command(cls, command: str)->str:
        """
        Execute a command on the device.
        :param command: The command to execute.
        :return: The output of the command.
        """
        try:
            cls.logger.debug(f"Executing command: {command}")
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            )
            stdout, _ = process.communicate()
            return stdout
        except Exception as e:
            cls.logger.error(f"[ERROR] Failed to run command {command} because {e}")
            return ""

