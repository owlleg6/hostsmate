import shutil
from pathlib import Path
from datetime import datetime

from khostman.formatter.formatter import Formatter
from khostman.utils.os_utils import OSUtils
from khostman.utils.logging_utils import LoggingUtils
from khostman.logger.logger import logger
from khostman.cli.prompt import UserInteraction
from khostman.unique_domains.unique_domains import UniqueDomains


class Writer:
    """A class responsible for writing operations related to the user's Hosts file.

    Attributes:
        hosts_path (pathlib.Path): a path to the system's hosts file
        hosts_new_path (pathlib.Path): a path to the new hosts file to be written with updated data
        domains_total_num (int): total number of unique blacklisted domains

    Methods:
        header() -> str
        write_to_hosts(self) -> None
        block_domain(self, str: blacklisted_domain) -> None
        whitelist_domain(self, str: whitelisted_domain) -> None
        create_backup(self) -> None
    """
    hosts_path: Path = OSUtils().path_to_hosts()
    hosts_new_path: Path = hosts_path.with_suffix('.temp')
    domains_total_num: int = UniqueDomains().count_domains()

    def header(self) -> str:
        """Return the common header for the Hosts file.

        This method uses the `UniqueDomains` class to count the number of domains,
        and the `datetime` module to get the current date.

        Returns:
            A string containing header for the Hosts file.
        """
        formatted_domains: str = '{:,}'.format(self.domains_total_num)
        current_date: str = datetime.now().strftime("%d-%b-%Y")
        return \
            f"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #                                                                   # #
# #   This file was generated with the Khostman app                   # #
# #                                                                   # #
# #   Created on {current_date.ljust(53)}# #
# #                                                                   # #
# #   Total number of unique entries: {formatted_domains.ljust(32)}# #
# #                                                                   # #
# #   Github repository: https://github.com/kravchenkoda/khostman     # #
# #                                                                   # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
\n
127.0.0.1 localhost
127.0.0.1 localhost.localdomain
127.0.0.1 local
255.255.255.255 broadcasthost
::1 localhost
::1 ip6-localhost
::1 ip6-loopback
fe80::1%lo0 localhost
ff00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts\n\n
# Start of the user's custom domains\n
\n# End of the user's custom domains\n\n
"""

    def build_hosts_file(self) -> None:
        """Write the list of unique blacklisted domains to the system's hosts file.

        This method uses the file path stored in the `hosts_path` attribute to open the
        hosts file and write the contents of the `blacklist_domains` list, which is
        obtained by calling the `get_unique_domains` method of the `UniqueDomains` class.
        The method also writes the header of the hosts file using the `header` method
        of the `Writer` class.
        """
        blacklist_domains: set[str] = UniqueDomains().get_unique_domains()

        try:
            print(f'Writing to {self.hosts_path}...')
            with open(self.hosts_path, 'w') as hosts:
                hosts.write(self.header())
                for line in blacklist_domains:
                    hosts.write(line)
        except OSError as e:
            print(f'Writing to {self.hosts_path} failed: {e}')
            logger.error(f'Writing to {self.hosts_path} failed: {e}')
            return
        logger.info(f'Hosts file at {self.hosts_path} was created/updated. '
                    f'Blacklisted {self.domains_total_num} unique domains.')
        print(f'Done. Blacklisted {self.domains_total_num} unique domains.\n'
              f'Enjoy the browsing!')

    def block_domain(self, blacklisted_domain: str) -> None:
        """Blacklist the given domain by writing it to the user's custom domains section of the
        Hosts file with 0.0.0.0 prefix.

        Args:
            blacklisted_domain (str): domain name to be added to the Hosts file
        """
        blacklisted_domain = Formatter().strip_domain_prefix(blacklisted_domain)
        domain_added = False

        try:
            with open(self.hosts_path, 'r') as hosts_old:
                with open(self.hosts_new_path, 'w') as hosts_new:
                    for line in hosts_old:
                        hosts_new.write(line)
                        if not domain_added and line.startswith("# Start"):
                            hosts_new.write(f'\n0.0.0.0 {blacklisted_domain}')
                            domain_added = True
                            print(f'"{blacklisted_domain}" domain name has been blacklisted')
                            logger.info(f'"{blacklisted_domain}" domain name has been blacklisted')
        except OSError as e:
            print(f'Operation failed: {e}')
            logger.error(f'Operation failed: {e}')
            return

        self.hosts_path.unlink()
        self.hosts_new_path.rename(self.hosts_path)

    @LoggingUtils.func_and_args_logging
    def whitelist_domain(self, whitelisted_domain: str) -> None:
        """Remove the given domain name from the blacklisted domains in the system's Hosts file if it is present.

        Args:
            whitelisted_domain (str): The domain to be whitelisted.
        """
        try:
            with open(self.hosts_new_path, 'w') as hosts_new:
                with open(self.hosts_path, 'r') as hosts_old:
                    whitelisted_domain = Formatter().strip_domain_prefix(whitelisted_domain)
                    found = False
                    for line in hosts_old:
                        if not found and whitelisted_domain in line:
                            found = True
                            continue
                        hosts_new.write(line)
        except OSError as e:
            print(f'Operation failed: {e}')
            logger.error(f'Operation failed: {e}')
            return

        if not found:
            print(f"No occurrence of '{whitelisted_domain}'"
                  f" found in file '{self.hosts_path}'")
            logger.info(f"No occurrence of '{whitelisted_domain}'"
                        f" found in file '{self.hosts_path}'")
        else:
            logger.info(f'"{whitelisted_domain}" has been whitelisted')

        self.hosts_path.unlink()
        self.hosts_new_path.rename(self.hosts_path)

    @LoggingUtils.func_and_args_logging
    def create_backup(self) -> None:
        """Create the backup of the user's original Hosts file in the specified directory.

        Backup path is obtained by calling ask_backup_directory method of the UserInteraction class.
        """
        backup_path: str = UserInteraction().ask_backup_directory()
        if not backup_path:
            return
        backup_hosts: Path = Path(backup_path) / 'hosts_backup'

        try:
            with self.hosts_path.open('rb') as src, backup_hosts.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            print(f'Backup file was created here: {backup_path}')
            logger.info('Backup of the original Hosts'
                        f' file was created at: {backup_path}')
        except OSError as e:
            logger.error(f'Error creating backup: {e}')
            print(f'Error creating backup: {e}')
