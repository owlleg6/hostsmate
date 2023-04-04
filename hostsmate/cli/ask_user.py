from logging import Logger
from pathlib import Path

from hostsmate.utils.os_utils import OSUtils
from hostsmate.logger.logger import HostsLogger


class AskUser:
    """A class for prompting the user via the command line interface.

    Methods:
        ask_backup_directory() -> str
        ask_autorun_frequency() -> str
        ask_if_backup_needed() -> bool
    """
    hosts_path: Path = OSUtils().path_to_hosts()
    wrong_input = 'Unrecognized input. Try again.\n'

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def check_hosts_existence(self) -> None:
        """Helper method to verify whether the hosts file exists.

        Raises:
            SystemExit: if the hosts file is not exists.
        """
        if not self.hosts_path.exists():
            print(f'No Hosts file has been found in '
                  f'{self.hosts_path.parent}')
            self.logger.info(f'No Hosts file in '
                             f'{self.hosts_path.parent}')
            raise SystemExit

    def ask_backup_directory(self) -> Path:
        """Prompt the user to select a backup directory and return the path.

        Returns:
            Path: The selected backup directory path.

        Raises:
            SystemExit: if specified directory is not exists.
        """
        backup_dir: str = input('Please enter a path to the directory where '
                                'to backup the original Hosts file: \n')
        if not backup_dir:
            print(self.wrong_input)
            self.ask_backup_directory()

        backup_dir: Path = Path(backup_dir).resolve()
        if not backup_dir.is_dir():
            self.logger.error(f'No such directory:\n{backup_dir}')
            raise SystemExit(f'No such directory:\n{backup_dir}'
                             '\nVerify the path and try again.')
        self.logger.info(f'Backup dir: {backup_dir}')
        return backup_dir

    def ask_autorun_frequency(self) -> str:
        """Prompt the user to select the frequency of autorun for Khostman.

        Returns:
            str: The selected autorun frequency ('1', '2', or '3').

        Raises:
            SystemExit: if the user entered "q"
        """
        freq_map: dict = {
            '1': 'daily',
            '2': 'weekly',
            '3': 'monthly'
        }

        while True:
            frequency: str = input(
                'How often do you want to autorun Khostman to update your '
                'Hosts file?\n'
                '(enter 1, 2 or 3)\n'
                '1. Daily\n'
                '2. Weekly\n'
                '3. Monthly\n'
                'Enter "q" to quit.\n'
            )
            if frequency.lower() == 'q':
                raise SystemExit
            if frequency in ['1', '2', '3']:
                self.logger.info(f'Chosen autorun frequency: '
                                 f'{freq_map[frequency]}')
                return frequency
            else:
                print(self.wrong_input)

    def ask_if_backup_needed(self) -> bool:
        """Prompts the user to select whether to backup the original Hosts file.

        Returns:
            bool: True if the user chooses to backup, False otherwise.
        """
        self.check_hosts_existence()

        answers: dict = {
            'y': True,
            'n': False
        }
        choice: str = input('Do you want to backup your original '
                            'Hosts file? (y or n): ').lower()

        if choice not in answers.keys():
            print(self.wrong_input)
            return self.ask_if_backup_needed()

        answer: bool = answers[choice]
        self.logger.info(f"User's choice on backup: {answer}")
        return answer
