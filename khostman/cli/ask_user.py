from tkinter.filedialog import askdirectory
from os.path import isfile

from khostman.utils.logging_utils import LoggingUtils
from khostman.logger.logger import logger


class AskUser:
    """A class for prompting the user via the command line interface.

    Methods:
        ask_backup_directory() -> str
        ask_autorun_frequency() -> str
        ask_if_backup_needed() -> bool
    """
    @staticmethod
    @LoggingUtils.func_and_args_logging
    def ask_backup_directory() -> str:
        """Prompt the user to select a backup directory and returns the path.

        Returns:
            str: The selected backup directory path.
        """
        backup_path = askdirectory(title='Select Backup Directory')  # shows dialog box and returns the path
        return backup_path

    @staticmethod
    def ask_autorun_frequency() -> str:
        """Prompts the user to select the frequency of autorun for Khostman.

        Returns:
            str: The selected autorun frequency ('1', '2', or '3').
        """
        wrong_input = 'Unrecognized input. Try again.\n'
        while True:
            frequency = input(
                'How often do you want to autorun Khostman to update your Hosts file?\n'
                '(enter 1, 2 or 3)\n'
                '1. Daily\n'
                '2. Weekly\n'
                '3. Monthly\n'
                'Enter "q" to quit.\n'
            )
            if frequency.lower() == 'q':
                exit()
            if frequency in ['1', '2', '3']:
                return frequency
            else:
                print(wrong_input)

    @staticmethod
    def ask_if_backup_needed() -> bool:
        """Prompts the user to select whether or not to backup the original Hosts file.

        Returns:
            bool: True if the user chooses to backup, False otherwise.
        """
        need_backup = input('Do you want to backup your original Hosts file? '
                            '(y or n)').lower()
        while True:
            if not isfile('hosts'):
                print('No Hosts file has been found in /etc/hosts')
                logger.info('No Hosts file has been found in /etc/hosts')
                return False
            elif need_backup == 'y':
                return True
            elif need_backup == 'n':
                logger.info('The user refused to backup the original file')
                return False
            else:
                logger.info('Unrecognizable user input')
                need_backup = input('Your answer is not recognised.'
                                    ' Please enter "y" or "n" '
                                    'to confirm your choice: ')
