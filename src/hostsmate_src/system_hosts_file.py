import shutil
import sys
import tempfile
from logging import Logger
from pathlib import Path
from datetime import date, datetime

from hostsmate_src.domains_extractor import DomainsExtractor
from hostsmate_src.logger import HostsLogger
from hostsmate_src.sources.blacklist_sources import BlacklistSources
from hostsmate_src.unique_blacklisted_domains import UniqueBlacklistedDomains
from utils.os_utils import OSUtils
from utils.str_utils import StringUtils


class SystemHostsFile:
    """
    The SystemHostsFile class represents the system's hosts file.

    Methods:
        _get_header() -> str
        _get_user_custom_domains -> set[str]
        add_blacklisted_domain(domain: str) -> None
        remove_domain(domain: str) -> None
        create_backup(backup_path: str| Path) -> None
        build() -> None

    Properties:
        original_path (Path): The path to the hosts file on the current system.
        renamed_path (Path): The path to the temporary renamed hosts file.
        _header_path (Path): The path to the hosts static header file.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    @property
    def _header_path(self) -> Path:
        project_root: Path = OSUtils().get_project_root()
        return project_root / 'resources' / 'hosts_header'

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
            return Path('/etc/hosts')
        else:
            raise SystemExit('Sorry, your platform is not supported.')

    @property
    def renamed_path(self) -> Path:
        """Get the path to the temporary renamed hosts file."""
        renamed_path: Path = self.original_path.with_suffix('.tmp')
        return renamed_path

    def _get_user_custom_domains(self) -> set[str]:
        """
        Extract user's custom domains from the user's custom domains
        Hosts file section.

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
        """Blacklist the given domain by writing it to the user's custom domains
        section of the Hosts file with 0.0.0.0 prefix.

        Args:
            domain (str): domain name to be added to the Hosts file
        """
        domain: str = StringUtils.strip_domain_prefix(domain)
        domain_added: bool = False

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

    def remove_domain(self, domain: str) -> None:
        """Remove the given domain name from the blacklisted domains in
        the system's Hosts file if it is present.

        Args:
            domain (str): The domain to be whitelisted.
        """
        with open(self.renamed_path, 'w') as hosts_new:
            with open(self.original_path, 'r') as hosts_old:
                domain: str = StringUtils.strip_domain_prefix(domain)
                found: bool = False
                for line in hosts_old:
                    if not found and domain in line:
                        found = True
                        continue
                    hosts_new.write(line)
        self.renamed_path.rename(self.original_path)

    def create_backup(self, backup_path: str | Path) -> Path:
        """Create the backup of the user's original Hosts file in the specified
        directory.

        Args:
            backup_path (str| Path): Path to the backup directory

        Returns:
            A Path object representing an absolute path to the backup file.
        """
        backup_path = Path(backup_path) / f'hosts_backup' \
                                          f'{datetime.now().strftime("%d_%m_%Y")}'

        with self.original_path.open('rb') as src,\
                backup_path.open('wb') as dst:
            shutil.copyfileobj(src, dst)
        print(f'Backup file location: {backup_path}')
        self.logger.info(f'Backup file is {backup_path}')
        return backup_path

    def _get_header(self) -> str:
        """Add a header to the hosts file using the template file located at
        self.__header_path.

        Returns:
            A string containing the header content.
        """
        with open(self._header_path, 'r') as f:
            template: str = f.read()

        formatted_domains: str = StringUtils.sep_num_with_commas(
            UniqueBlacklistedDomains().amount
        )
        current_date: date = date.today()
        custom_domains: str = '\n'.join(self._get_user_custom_domains())

        output: str = template.format(
            date=current_date,
            num_entries=formatted_domains,
            custom_domains=custom_domains
        )
        return output

    def _build(self) -> None:
        """Build the system's hosts file.

        Write header, user's custom blacklisted domains (if present in the
        current hosts file), populate with parsed unique blacklisted domains.
        """
        blacklist_domains: set[str] = UniqueBlacklistedDomains().items
        formatted_domains_total_num: str = StringUtils.sep_num_with_commas(
            UniqueBlacklistedDomains().amount
        )
        header: str = self._get_header()

        print('Building new Hosts file...')
        with open(self.original_path, 'w') as hosts:
            hosts.write(header)
            for line in blacklist_domains:
                hosts.write(line)

        self.logger.info(f'Hosts file at {self.original_path} '
                         f'was created/updated. '
                         f'Added {formatted_domains_total_num} entries.')

        print(f'Done. Blacklisted {formatted_domains_total_num} unique domains.\n'
              f'Enjoy the browsing!')

    def update_with_new_domains(self) -> None:
        """
        Collect domain entries from raw sources, format them, remove
        duplicates, and write the resulting entries to the system hosts file.
        """
        with tempfile.NamedTemporaryFile(mode='a') as temp:
            BlacklistSources().append_sources_contents_to_file_concurrently(
                temp.name
            )
            DomainsExtractor(temp.name).extract_domain_to_unique_domains_set()
            self._build()
