import sys
from pathlib import Path
from logging import Logger

from hostsmate_src.cli.prompt import Prompt
from utils.os_utils import OSUtils
from hostsmate_src.logger import HostsLogger


class Autorunner:
    """A class responsible for setting up automatic update of the system's
     Hosts file with anacron by modifying /etc/anacrontab file.

    Attributes:
        hostsmate_executable (Path) = path to the app entry point.
        job_setter_sh_script_path (Path) = path to the anacron_job_setter.sh
        which sets up an anacron job.

    Methods:
        run_anacron_setter_sh_script(autorun_frequency: str) -> Bool:
        Run the anacron_job_setter.sh script.

        set_up_anacron_job() -> Bool: Sets up an anacron job to run the application
        on a specified schedule.
    """
    hostsmate_executable: Path = \
        OSUtils.get_project_root() / 'hostsmate_src' / 'execute.py'

    job_setter_sh_script_path: Path = \
        OSUtils.get_project_root() / 'resources' / 'anacron_job_setter.sh'

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def run_anacron_setter_sh_script(self, autorun_frequency: str) -> bool:
        """Run the anacron_job_setter.sh script.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.
        """
        command: list[str] = \
            [autorun_frequency, f'hostsmate --run']
        done: bool = OSUtils().execute_sh_command_as_root(
            self.job_setter_sh_script_path, command)
        if done:
            print('Autorunner has been set.')
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
            bool: True if the job setter script returned 0 status code.

        Raises:
            SystemExit: If the current operating system is not compatible with the
                feature or if the anacron dependency is not installed.
        """
        linux_or_bsd_platform: bool = OSUtils.ensure_linux_or_bsd(sys.platform)
        anacron_dependency_installed: bool = \
            OSUtils().is_shell_dependency_installed('anacron')

        Autorunner.job_setter_sh_script_path.chmod(1)

        if linux_or_bsd_platform and anacron_dependency_installed:
            autorun_frequency: str = Prompt().ask_autorun_frequency()

            self.run_anacron_setter_sh_script(
                autorun_frequency
            )
            self.logger.info('Anacron job has been set.')
            return True
        else:
            raise SystemExit('This feature is not supported for your '
                             'operating system or the anacron dependency '
                             'is not installed.')
