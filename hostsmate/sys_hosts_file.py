import sys
from logging import Logger
from pathlib import Path

from hostsmate.logger import HostsLogger


class SysHostsFile:
    """
        A class representing the system's hosts file.

    Methods:
        check_hosts_existence(): Verifies whether the hosts file exists on the system.

    Attributes:
        org_path (Path): The path to the hosts file on the current system.
        renamed_path (Path): The path to the temporary renamed hosts file.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    @property
    def org_path(self) -> Path:
        """Return the path to the hosts file on the current system.

        Returns:
            Path: The path to the hosts file.
        """
        platform: str = sys.platform

        if platform.startswith(
                (
                        'linux',
                        'freebsd',
                        'darwin',
                        'cygwin'
                )
        ):
            hosts_path: Path = Path('/etc/hosts')
            return hosts_path
        elif platform.startswith('win'):
            root_drive: str = Path(sys.executable).anchor
            hosts_path: Path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')
        self.logger.info(f'path to the hosts file is {hosts_path}')
        return hosts_path

    @property
    def renamed_path(self) -> Path:
        """Get the path to the temporary renamed hosts file."""
        renamed_path: Path = self.org_path / '.tmp'
        return renamed_path

    def check_hosts_existence(self) -> bool:
        """Verify whether the hosts file exists.

        Returns:
            bool: True if the system's hosts file exists, False otherwise.

        Raises:
            SystemExit: if the hosts file is not exists.
        """
        if not self.org_path.exists():
            print(f'No Hosts file found: {self.org_path}')
            self.logger.info(f'No Hosts file found: {self.org_path}')
            return False
        else:
            return True
