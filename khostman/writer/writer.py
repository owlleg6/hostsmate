import shutil
from socket import gethostname
from pathlib import Path

from khostman.formatter.formatter import Formatter
from khostman.utils.utils import func_and_args_logging, timer
from khostman.logger.logger import logger
from khostman.cli.prompt import UserInteraction


class Writer:
    _path = 'hosts'

    @staticmethod
    def add_header():
        header = "\n############   "
        "System-wide adblocker by Kravchenkoda. "
        "Inspired by Hosty"
        "   ############\n\n"
        "127.0.0.1 view-localhost\n"
        "127.0.0.1 localhost\n"
        f"127.0.1.1	{gethostname()}\n\n"

    def write_to_hosts(self, blacklist_domains: str) -> None:
        """Writes domains to the system's hosts file."""
        print('Writing to /etc/hosts...')
        with open(self._path, 'w') as hosts:
            for line in blacklist_domains:
                hosts.write(line)

        print(f'Blocked {len(blacklist_domains)} websites.')

    def block_domain(self, *args):
        with open(self._path, 'a+') as hosts:
            hosts.write("\n############   User's custom blocked hosts   ############\n\n")
            for website in args:
                hosts.write(f"0.0.0.0 {website}\n")

    @staticmethod
    @func_and_args_logging
    def whitelist_domain(whitelisted_url):
        hosts_path = Path('hosts')
        temp_hosts_path = hosts_path.with_suffix('.temp')

        with open(temp_hosts_path, 'w') as temp:
            with open(hosts_path, 'r') as original:
                whitelisted_url = Formatter().strip_domain_prefix(whitelisted_url)
                found = False
                for line in original:
                    if whitelisted_url in line:
                        found = True
                        continue
                    temp.write(line)

                if not found:
                    print(f"No occurrence of '{whitelisted_url}'"
                          f" found in file '{hosts_path}'")
                    logger.info(f"No occurrence of '{whitelisted_url}'"
                                f" found in file '{hosts_path}'")
        hosts_path.unlink()
        temp_hosts_path.rename(hosts_path)

    @timer
    @func_and_args_logging
    def create_backup(self):
        """Creates the backup of the user's original Hosts file"""
        original_hosts = Path(self._path)
        backup_path = UserInteraction().ask_backup_directory()
        if not backup_path:
            return
        backup_hosts = Path(backup_path) / 'hosts_backup'
        try:
            with original_hosts.open('rb') as src, backup_hosts.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            print(f'Backup file was created here: {backup_path}')
            logger.info('Backup of the original Hosts'
                        f' file was created at: {backup_path}')
        except OSError as e:
            logger.warning(f'Error creating backup: {e}')
            print(f'Error creating backup: {e}')
