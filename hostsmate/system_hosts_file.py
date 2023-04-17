import shutil
import sys
from logging import Logger
from pathlib import Path
from datetime import datetime

from hostsmate.logger import HostsLogger
from hostsmate.unique_blacklisted_domains import UniqueBlacklistedDomains
from utils.os_utils import OSUtils
from utils.str_utils import StringUtils


class SystemHostsFile:
    """
    The SystemHostsFile class represents the system's hosts file.

    Methods:
        __get_header() -> str
        __get_user_custom_domains -> set[str]
        add_blacklisted_domain(domain: str) -> None
        remove_domain(domain: str) -> None
        create_backup(backup_path: str) -> None
        build() -> None

    Properties:
        original_path (Path): The path to the hosts file on the current system.
        renamed_path (Path): The path to the temporary renamed hosts file.
        __header_path (Path): The path to the hosts file static header file.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    @property
    def __header_path(self) -> Path:
        project_root = OSUtils().get_project_root()
        return project_root / 'hostsmate' / 'resources' / 'hosts_header'

    @property
    def original_path(self) -> Path:
        """Return the path to the hosts file on the current system.

        Returns:
            Path: The path to the hosts file.
        """
        platform: str = sys.platform

        if platform.startswith(
                (
                        'linux',
                        'freebsd',
                        'darwin',
                        'cygwin'
                )
        ):
            hosts_path: Path = Path('/etc/hosts')
            return hosts_path
        elif platform.startswith('win'):
            root_drive: str = Path(sys.executable).anchor
            hosts_path: Path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')

        self.logger.info(f'path to the hosts file is {hosts_path}')
        return hosts_path

    @property
    def renamed_path(self) -> Path:
        """Get the path to the temporary renamed hosts file."""
        renamed_path: Path = self.original_path.with_suffix('.tmp')
        return renamed_path

    def __get_user_custom_domains(self) -> set[str]:
        """
        Extracts user's custom domains from the Hosts file.

        Returns:
            A set of strings representing user's custom domains.
        """
        users_custom_domains = set()
        if not self.original_path.exists():
            return users_custom_domains
        else:
            custom_domain_section = False
            with open(self.original_path) as f:
                for line in f:
                    if line.startswith('# Start'):
                        custom_domain_section = True
                    elif line.startswith('# End'):
                        custom_domain_section = False
                    elif custom_domain_section and line.strip():
                        users_custom_domains.add(line.strip())
        return users_custom_domains

    def add_blacklisted_domain(self, domain: str) -> None:
        """Blacklist the given domain by writing it to the user's custom domains section of the
        Hosts file with 0.0.0.0 prefix.

        Args:
            domain (str): domain name to be added to the Hosts file
        """
        domain: str = StringUtils.strip_domain_prefix(domain)
        domain_added: bool = False

        try:
            with open(self.original_path, 'r') as hosts_old:
                with open(self.renamed_path, 'w') as hosts_new:
                    for line in hosts_old:
                        hosts_new.write(line)
                        if not domain_added and line.startswith('# Start'):
                            hosts_new.write(f'\n0.0.0.0 {domain}')
                            domain_added = True
                            print(f'"{domain}" domain name has been blacklisted')
                            self.logger.info(f'"{domain}" domain name has been blacklisted')
                            self.renamed_path.rename(self.original_path)
        except OSError as e:
            print(f'Operation failed: {e}')
            self.logger.error(f'Operation failed: {e}')

    def remove_domain(self, domain: str) -> None:
        """Remove the given domain name from the blacklisted domains in
        the system's Hosts file if it is present.

        Args:
            domain (str): The domain to be whitelisted.
        """
        try:
            with open(self.original_path, 'w') as hosts_new:
                with open(self.renamed_path, 'r') as hosts_old:
                    domain: str = StringUtils.strip_domain_prefix(domain)
                    found: bool = False
                    for line in hosts_old:
                        if not found and domain in line:
                            found = True
                            continue
                        hosts_new.write(line)
        except OSError as e:
            print(f'Operation failed: {e}')
            self.logger.error(f'Operation failed: {e}')

    def create_backup(self, backup_path: str) -> None:
        """Create the backup of the user's original Hosts file in the specified
        directory.

        Args:
            backup_path (str): Path to the backup directory
        """
        try:
            with self.original_path.open('rb') as src, backup_path.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            print(f'Backup file is: {backup_path}')
            self.logger.info(f'Backup file is {backup_path}')
        except OSError as e:
            self.logger.error(f'Error creating backup: {e}')
            print(f'Error creating backup.')

    def __get_header(self) -> str:
        """Adds a header to the hosts file using the template file located at
        self.__header_path.

        Returns:
            A string containing the header content.
        """
        with open(self.__header_path, 'r') as f:
            template: str = f.read()

        formatted_domains: str = StringUtils.sep_num_with_commas(
            UniqueBlacklistedDomains().amount
        )
        current_date: str = datetime.now().strftime("%d-%b-%Y")
        custom_domains: str = '\n'.join(self.__get_user_custom_domains())

        output: str = template.format(
            date=current_date,
            num_entries=formatted_domains,
            custom_domains=custom_domains
        )

        return output

    def build(self) -> None:
        """Build the system's hosts file.

        Write header, user's custom blacklisted domains (if present in the
        current hosts file), populate with parsed unique blacklisted domains.
        """
        blacklist_domains: set[str] = UniqueBlacklistedDomains().items
        domains_total_num: int = UniqueBlacklistedDomains().amount

        try:
            print(f'Building new Hosts file...')
            with open(self.original_path, 'w') as hosts:
                hosts.write(self.__get_header())
                for line in blacklist_domains:
                    hosts.write(line)
        except OSError as e:
            print(f'Writing to {self.original_path} failed: {e}')
            self.logger.error(f'Writing to {self.original_path} failed: {e}')
            return

        self.logger.info(f'Hosts file at {self.original_path} '
                         f'was created/updated. '
                         f'Added {domains_total_num} entries.')

        print(f'Done. Blacklisted {domains_total_num} unique domains.\n'
              f'Enjoy the browsing!')
