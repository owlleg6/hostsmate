import subprocess
from pathlib import Path

from khostman.cli.prompt import UserInteraction
from khostman.utils.data_utils import OSUtils


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

    @staticmethod
    def check_anacron_dependency() -> None:
        """
        Verify whether anacron package is installed on the system, exit if not.
        """
        anacron: subprocess.CompletedProcess = subprocess.run(['which', 'anacron'], capture_output=True)
        if not anacron.stdout:
            exit("Please install 'anacron' dependency and try again.")

    def add_exec_permissions(self):
        """Add executable permissions to the anacron job setter bash script."""
        subprocess.run(['chmod', '+x', self.job_setter_sh])

    def set_anacron_job(self):
        """Run the anacron_job_setter.sh script."""

        self.check_anacron_dependency()
        autorun_frequency = UserInteraction.ask_autorun_frequency()
        self.add_exec_permissions()
        subprocess.run(['bash',
                        self.job_setter_sh,
                        autorun_frequency,
                        f'python3 {self.khostman_app} --go'
                        ])
