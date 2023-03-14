from khostman.logger.logger import logger
from tkinter.filedialog import askdirectory
from os.path import isfile

from khostman.utils.utils import func_and_args_logging

class UserInteraction:

    @func_and_args_logging
    def ask_backup_directory(self) -> str:
        backup_path = askdirectory(title='Select Backup Directory')  # shows dialog box and returns the path
        return backup_path

    def ask_if_backup_needed(self):
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

    def greeting(self):

        initial_choice = input(
            'Welcome to the system-wide ad blocker by Kravchenkoda.\n'
            'Protect yourself from malware, tracking, ads and spam.\n'
            '1 400 000+ malicious domains from almost 50 sources that update regularly.\n'
            'For more details type "help". To start type "go": ')

        if initial_choice == 'help':
            pass
        elif initial_choice == 'go':
            self.ask_if_backup_needed()