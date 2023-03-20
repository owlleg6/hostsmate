from pathlib import Path
import subprocess

from khostman.cli.prompt import UserInteraction


class Autorunner:
    khostman_app = Path(__file__).resolve().parents[2] / 'app.py'
    job_setter_sh = Path(__file__).resolve().parents[2] / 'anacron_job_setter.sh'

    def __init__(self):
        self.check_anacron_dependency()
        self.autorun_frequency = UserInteraction.ask_autorun_frequency()

    @staticmethod
    def check_anacron_dependency() -> None:
        """
        Exit if anacron package is not installed.
        """
        anacron = subprocess.run(['which', 'anacron'], capture_output=True)
        if not anacron.stdout:
            exit("Please install 'anacron' dependency and try again.")

    def add_exec_permissions(self):
        subprocess.run(['chmod', '+x', self.job_setter_sh])

    def set_anacron_job(self):
        self.add_exec_permissions()
        subprocess.run(['bash',
                        self.job_setter_sh,
                        self.autorun_frequency,
                        f'"python3 {self.khostman_app} --go"'])
