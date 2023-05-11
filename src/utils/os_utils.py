import pathlib
import subprocess
from pathlib import Path

from hostsmate_src import logger as logger


class OSUtils:
    """
    This class contains utility methods for operating system-related tasks.

    Methods:
        get_project_root() -> Path: Return the root directory of the project.

        ensure_linux_or_bsd(platform: str) -> Bool: Ensure that the application
        is running on Linux or FreeBSD platform.

        execute_sh_command_as_root(program: str | Path,
                                   cli_args: list[int | float | str]
                                  ) -> Bool: Execute shell command with sudo.

        is_shell_dependency_installed(dependency: str) -> Bool: return True
        if dependency installed, False otherwise.
   """

    def __init__(self):
        self.logger = logger.HostsLogger().create_logger('Utils')

    @staticmethod
    def get_project_root() -> pathlib.Path:
        """
        Return the root directory of the project.

        The root directory is defined as the parent directory of the directory
        containing the module that this method is called from.

        Returns:
            pathlib.Path: The root directory of the project.
        """
        project_root: pathlib.Path = Path(__file__).resolve().parents[1]
        return project_root

    @staticmethod
    def ensure_linux_or_bsd(platform) -> bool:
        """Ensure that the current operating system is compatible with the
        feature (Linux and FreeBSD), exit if it is not.

        Returns:
            bool: True if platform is linux or freebsd, False otherwise.
        """
        allowed_platforms: list[str] = ['linux', 'freebsd']

        return platform in allowed_platforms

    def execute_sh_command_as_root(
            self,
            program: str | Path,
            cli_args: list[int | float | str]
    ) -> bool:
        """
        Execute a shell command as root user using sudo.

        Args:
            program (str): The name of the shell command to execute.
            cli_args (list): A list of string arguments to pass to the command.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.

        Raises:
            SystemExit: if there is the error while executing command.
        """
        command: list[str | Path] = ['sudo', program]
        command.extend(cli_args)
        try:
            process: subprocess.CompletedProcess = subprocess.run(command)
        except subprocess.SubprocessError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')
        return_code = process.returncode
        self.logger.info(f'return code: {return_code}')
        return process.returncode == 0

    def is_shell_dependency_installed(self, dependency: str) -> bool:
        """Verify whether the dependency is installed on the system.

        Args:
            dependency (str): dependency name to be verified.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.

        Raises:
            SystemExit: if there is the error while executing command.
        """
        try:
            command: subprocess.CompletedProcess = subprocess.run(
                ['which', dependency],
                stdout=subprocess.DEVNULL
            )
        except subprocess.SubprocessError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')
        return_code = command.returncode
        self.logger.info(f'return code: {return_code}')
        return command.returncode == 0
