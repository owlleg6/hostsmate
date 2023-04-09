import subprocess
from pathlib import Path
from logging import Logger

from hostsmate.cli.ask_user import AskUser
from hostsmate.utils.data_utils import OSUtils
from hostsmate.logger import HostsLogger


class Autorunner:
    """A class responsible for setting up automatic update of the system's
     Hosts file.

    Attributes:
        hostsmate_app (Path) = path to the hostsmate.py file.
        job_setter_sh_script (Path) = path to the anacron_job_setter.sh which sets up
        an anacron job (bash only).

    """
    hostsmate_app: Path = OSUtils.get_project_root() / 'hostsmate.py'
    job_setter_sh_script: Path = OSUtils.get_project_root() / 'anacron_job_setter.sh'

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def set_anacron_job(self) -> bool:
        """Run the anacron_job_setter.sh script.

        Returns bool:
                    True if the anacron job set.
                    False otherwise.
        """
        if OSUtils.ensure_linux_or_bsd() and \
                OSUtils().is_shell_dependency_installed('anacron'):

            autorun_frequency: str = AskUser().ask_autorun_frequency()
            OSUtils().add_exec_permissions(self.job_setter_sh_script)

            command = [autorun_frequency, f'python3 {self.hostsmate_app} --go']

            OSUtils().execute_sh_command_as_root(
                self.job_setter_sh_script, command)

        return False
