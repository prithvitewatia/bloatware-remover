import logging
import subprocess


class CommandManager:
    logger = logging.getLogger(__name__)

    @classmethod
    async def execute_command(cls, command: str) -> str:
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
