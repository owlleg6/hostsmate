import subprocess
import sys
from pathlib import Path

from khostman.cli.ask_user import AskUser
from khostman.utils.data_utils import OSUtils
from khostman.logger.logger import logger


class Autorunner:
    """A class responsible for setting up automatic update of the system's
     Hosts file.

    Attributes:
        khostman_app (Path) = path to the khostman.py file.
        job_setter_sh (Path) = path to the anacron_job_setter.sh which sets up
        an anacron job for Linux (bash only).

    """
    khostman_app: Path = OSUtils.get_project_root() / 'app.py'
    job_setter_sh: Path = OSUtils.get_project_root() / 'anacron_job_setter.sh'

    def __init__(self):
        self.ensure_os_compatibility()

    @staticmethod
    def ensure_os_compatibility():
        """Ensure that the current operating system is compatible with the
        autorunner feature (Linux and FreeBSD), exit if it is not.

        Raises:
            SystemExit: If the current operating system is not in the list of
            allowed platforms.
        """
        platform: str = sys.platform
        allowed_platforms: list[str] = ['linux', 'freebsd']

        if platform not in allowed_platforms:
            sys.exit('This feature in not supported for your operating system.')

    @staticmethod
    def check_anacron_dependency() -> None:
        """
        Verify whether anacron package is installed on the system, exit if not.
        """
        try:
            anacron: subprocess.CompletedProcess = subprocess.run(
                ['which', 'anacron'],
                capture_output=True
            )
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            logger.error(f'Operation failed: {e}')

        if not anacron.stdout:
            exit("Please install 'anacron' dependency and try again.")

    def add_exec_permissions(self):
        """Add executable permissions to the anacron job setter bash script."""
        try:
            subprocess.run(
                ['chmod',
                 '+x',
                 self.job_setter_sh
                 ]
            )
            logger.debug(f'executable permissions added to {self.job_setter_sh}')
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            logger.error(f'Operation failed: {e}')

    def set_anacron_job(self):
        """Run the anacron_job_setter.sh script."""

        self.check_anacron_dependency()
        autorun_frequency: str = AskUser.ask_autorun_frequency()
        self.add_exec_permissions()
        try:
            subprocess.run(['bash',
                            self.job_setter_sh,
                            autorun_frequency,
                            f'python3 {self.khostman_app} --go'
                            ])
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            logger.error(f'Operation failed: {e}')
