import shutil
from socket import gethostname
from pathlib import Path
from khostman.formatter.formatter import Formatter
from khostman.utils.utils import timer
from khostman.utils.utils import func_and_args_logging
from khostman.logger.logger import logger
from khostman.unformatted_domains.unformatted_domains import UnformattedDomains


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
                    print(f"No occurrence of '{whitelisted_url}' found in file '{hosts_path}'")
                    logger.info(f"No occurrence of '{whitelisted_url}' found in file '{hosts_path}'")
        hosts_path.unlink()
        temp_hosts_path.rename(hosts_path)

    @func_and_args_logging
    def create_backup(self, backup_path):
        """Creates the backup of the user's original Hosts file"""

        original_hosts = Path(self._path)
        backup_path = Path(backup_path)

        try:
            # use shutil.copy() to copy the file
            shutil.copy(original_hosts, backup_path)
            print(f'Backup created: {backup_path}')
        except OSError as e:
            print(f'Error creating backup: {e}')
            backup_path = None

        return backup_path
