import logging

from .cmd_manager import CommandManager


class PackageManager:

    logger = logging.getLogger(__name__)

    @classmethod
    async def get_installed_packages(cls) -> list[str]:
        """
        Get a list of installed packages on the device.
        :return: A list of installed packages that match the filter.
        """
        cmd = "adb shell pm list packages"
        stdout = await CommandManager.execute_command(cmd)
        if not stdout:
            cls.logger.warning("No packages found")
            return []

        return [
            package.strip().replace("package:", "", 1)
            for package in stdout.split("\n")
            if package.strip()
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
