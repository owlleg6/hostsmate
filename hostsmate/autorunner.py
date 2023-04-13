import sys
from pathlib import Path
from logging import Logger

from hostsmate.cli.ask_user import AskUser
from hostsmate.utils.os_utils import OSUtils
from hostsmate.logger import HostsLogger


class Autorunner:
    """A class responsible for setting up automatic update of the system's
     Hosts file with anacron by modifying /etc/anacrontab file.

    Attributes:
        hostsmate_app (Path) = path to the hostsmate.py file.
        job_setter_sh_script_path (Path) = path to the anacron_job_setter.sh
        which sets up an anacron job (bash only).
    """
    hostsmate_app: Path = OSUtils.get_project_root() / 'hostsmate.py'
    job_setter_sh_script_path: Path = \
        OSUtils.get_project_root() / 'anacron_job_setter.sh'

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def run_anacron_setter_sh_script(self, autorun_frequency) -> bool:
        """Run the anacron_job_setter.sh script.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.
        """
        command = [autorun_frequency, f'python3 {self.hostsmate_app} --go']
        done: bool = OSUtils().execute_sh_command_as_root(
            self.job_setter_sh_script_path, command)
        if done:
            print('Autorunner has been set')
            self.logger.info(f'Executed with 0 status code: '
                             f'{self.job_setter_sh_script_path}')
        else:
            print('Operation failed')
            self.logger.info(f'Executed with non-zero status code: '
                             f'{self.job_setter_sh_script_path}')
        return done

    def set_up_anacron_job(self) -> bool:
        """Sets up an anacron job to run the application on a specified schedule.

        Returns:
            bool: True if

        Raises:
            SystemExit: If the current operating system is not compatible with the
                feature or if the anacron dependency is not installed.
        """
        linux_or_bsd_platform: bool = OSUtils.ensure_linux_or_bsd(sys.platform)
        anacron_dependency_installed: bool = \
            OSUtils().is_shell_dependency_installed('anacron')

        if linux_or_bsd_platform and anacron_dependency_installed:
            autorun_frequency: str = AskUser().ask_autorun_frequency()

            OSUtils().add_exec_permissions(
                Autorunner.job_setter_sh_script_path
            )

            self.run_anacron_setter_sh_script(
                autorun_frequency
            )
            self.logger.info('Anacron job has been set.')
            return True
        else:
            raise SystemExit('This feature is not supported for your '
                             'operating system or the anacron dependency '
                             'is not installed.')
