from tkinter.filedialog import askdirectory
from logging import Logger
from pathlib import Path

from khostman.utils.os_utils import OSUtils
from khostman.utils.logging_utils import LoggingUtils
from khostman.logger.logger import HostsLogger


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

    def ask_backup_directory(self) -> Path:
        """Prompt the user to select a backup directory and return the path.

        Returns:
            Path: The selected backup directory path.

        Raises:
            SystemExit: if specified directory is not exists.
        """
        while True:
            backup_dir: str = input('Please enter a path to the directory where '
                                    'to backup the original Hosts file: \n')
            if not backup_dir:
                print(self.wrong_input)
                self.ask_backup_directory()

            backup_dir: Path = Path(backup_dir).resolve()
            if not backup_dir.is_dir():
                raise SystemExit(f'No such directory:\n{backup_dir}'
                                 '\nVerify the path and try again.')
            return backup_dir

    def ask_autorun_frequency(self) -> str:
        """Prompts the user to select the frequency of autorun for Khostman.

        Returns:
            str: The selected autorun frequency ('1', '2', or '3').
        """

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
                exit()
            if frequency in ['1', '2', '3']:
                self.logger.info(f'Chosen autorun frequency: {frequency}')
                return frequency
            else:
                print(self.wrong_input)

    def ask_if_backup_needed(self) -> bool:
        """Prompts the user to select whether to backup the original Hosts file.

        Returns:
            bool: True if the user chooses to backup, False otherwise.
        """
        need_backup: str = input('Do you want to backup your original '
                                 'Hosts file? (y or n)').lower()
        while True:
            if not self.hosts_path.exists():
                print(f'No Hosts file has been found in '
                      f'{self.hosts_path.parent}')
                self.logger.info(f'No Hosts file in '
                                 f'{self.hosts_path.parent}')
                return False
            elif need_backup == 'y':
                return True
            elif need_backup == 'n':
                self.logger.info('The user refused to backup the original file')
                return False
            else:
                self.logger.info('Unrecognizable user input')
                need_backup = input('Your answer is not recognised.'
                                    ' Please enter "y" or "n" '
                                    'to confirm your choice: ')
