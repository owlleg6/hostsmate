import ctypes
import pathlib
import sys
from os import getuid
from os.path import join
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from khostman.logger.logger import logger
from khostman.utils.utils import Utils


class OSUtils(Utils):
    """
    This class contains utility methods for operating system-related tasks.

    Methods:
        ensure_root_privileges(): Ensure that the application is running with root/administrator privileges. Exit if it is not.
        get_platform(): Returns a string indicating the platform of the operating system that the code is running on.
        mk_tmp_hex_file(): Create a temporary file path using a random hexadecimal UUID.
        path_to_hosts(): Return the path to the hosts file on the current system.
    """

    @staticmethod
    def ensure_root_privileges():
        """
        Ensure that the application is running with root/administrator privileges. Exit if it is not.

        Raises:
        SystemExit: If the application is not running with root/administrator privileges.
        """
        try:
            root = getuid() == 0
        except AttributeError:
            root = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if not root:
            logger.info('Not running as root. Exiting.')
            exit('Please run the application as a '
                 'root/administrator to continue.')

    @staticmethod
    def get_project_root() -> pathlib.Path:
        """
        Returns the root directory of the project.

        The root directory is defined as the parent directory of the directory containing
        the module that this method is called from.

        Returns:
            pathlib.Path: The root directory of the project.
        """
        project_root = Path(__file__).resolve().parents[2]
        return project_root

    @staticmethod
    def get_platform():
        """
        Returns a string indicating the platform of the operating system that the code is running on.

        Returns:
        str: A string that can be one of the following:
         - 'unix_like' if the code is running on a Linux, macOS, or FreeBSD system
         - 'windows' if the code is running on a Windows system
        """
        platform = sys.platform
        if platform.startswith('linux') \
                or platform.startswith('darwin') \
                or platform.startswith('freebsd'):
            platform = 'unix_like'
        elif platform.startswith('win'):
            platform = 'windows'
        logger.info(platform)
        return platform

    @staticmethod
    def mk_tmp_hex_file() -> str:
        """Create a temporary file path using a random hexadecimal UUID.

        Returns:
            str: The absolute path of the temporary file.
        """
        tmp = join(gettempdir(), uuid4().hex)
        return tmp

    def path_to_hosts(self) -> Path:
        """Return the path to the hosts file on the current system.

        Returns:
            Path: The path to the hosts file.
        """
        platform = self.get_platform()
        if platform == 'unix_like':
            hosts_path = Path('/etc/hosts')
            return hosts_path
        elif platform == 'windows':
            root_drive = Path(sys.executable).anchor
            hosts_path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')
            return hosts_path
