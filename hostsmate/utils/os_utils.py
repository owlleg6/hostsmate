import ctypes
import pathlib
import sys
from os import getuid
from os.path import join
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from hostsmate.utils.utils import Utils
import hostsmate.logger.logger as l


class OSUtils(Utils):
    """
    This class contains utility methods for operating system-related tasks.

    Methods:
        ensure_root_privileges(): Ensure that the application is running with
        root/administrator privileges. Exit if it is not.

        get_project_root(): Return the root directory of the project.

        mk_tmp_hex_file(): Create a temporary file path using a random
        hexadecimal UUID.

        path_to_hosts(): Return the path to the hosts file on the current system.
    """

    def __init__(self):
        self.logger = l.HostsLogger().create_logger('Utils')

    def ensure_root_privileges(self):
        """
        Ensure that the application is running with root/administrator privileges. Exit if it is not.

        Raises:
        SystemExit: If the application is not running with root/administrator privileges.
        """
        try:
            root: bool = getuid() == 0
        except AttributeError:
            root: bool = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if not root:
            self.logger.info('Not running as root. Exiting.')
            exit('Please run the application as a '
                 'root/administrator to continue.')

    @staticmethod
    def get_project_root() -> pathlib.Path:
        """
        Return the root directory of the project.

        The root directory is defined as the parent directory of the directory containing
        the module that this method is called from.

        Returns:
            pathlib.Path: The root directory of the project.
        """
        project_root: pathlib.Path = Path(__file__).resolve().parents[2]
        return project_root


    def mk_tmp_hex_file(self) -> str:
        """Create a temporary file path using a random hexadecimal UUID.

        Returns:
            str: The absolute path of the temporary file.
        """
        tmp: str = join(gettempdir(), uuid4().hex)
        self.logger.info(f'Temporary file: path: {tmp}')
        return tmp

    def path_to_hosts(self) -> Path:
        """Return the path to the hosts file on the current system.

        Returns:
            Path: The path to the hosts file.
        """
        platform: str = sys.platform

        if platform.startswith(('linux', 'freebsd', 'darwin')):
            hosts_path: Path = Path('/etc/hosts')
            return hosts_path
        elif platform.startswith('win'):
            root_drive: str = Path(sys.executable).anchor
            hosts_path: Path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')
        else:
            exit('This operating system is not supported.')
        self.logger.info(f'path to the hosts file is {hosts_path}')
        return hosts_path
