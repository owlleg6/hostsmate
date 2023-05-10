from logging import Logger
import re
from pathlib import Path

from hostsmate_src.sources.whitelist_sources import WhitelistSources
from hostsmate_src.logger import HostsLogger
from hostsmate_src.unique_blacklisted_domains import UniqueBlacklistedDomains


class DomainsExtractor:
    """
    The DomainsExtractor class extracts domain names from a file containing raw
    blacklist sources contents.

    Attributes:
        localhost_ip (str): A string representing the IP address for localhost.
        non_routable_ip (str): A string representing a non-routable IP address.
        domain_regex (re.Pattern): A compiled regular expression pattern used to
        match domain names.

    Methods:
        extract_domain_if_starts_with_non_rout_ip(line: str) -> str
        extract_domain_if_starts_with_localhost_ip(line: str) -> str
        extract_domain_with_regex(line: str) -> str
        extract_domain_from_line(line: str) -> str
        extract_domain_to_unique_domains_set(file_path: str) -> None
    """

    localhost_ip: str = '127.0.0.1'
    non_routable_ip: str = '0.0.0.0'
    domain_regex: re.Pattern = re.compile('([a-z0-9-]+[.]+)+[a-z0-9-]+')

    def __init__(self, file_path):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)
        self.file_path: Path = Path(file_path)

    @staticmethod
    def _extract_domain_if_starts_with_non_rout_ip(line: str) -> str:
        """
        Extract domain if the line starts with a non-routable IP address
        (0.0.0.0) and return it.

        Args:
            line (str): A string representing a line in a file.

        Returns:
            A string representing the extracted domain name.

        """
        stripped_line: str = line.strip()
        domain = ' '.join(stripped_line.split(' ')[:2]) + '\n'
        return domain

    def _extract_domain_if_starts_with_localhost_ip(self, line: str) -> str:
        """
        Extract domain if the line starts with a localhost IP address (127.0.0.1)
        and return it.

        Args:
            line (str): A string representing a line in a file.

        Returns:
            A string representing the extracted domain name.

        """
        try:
            stripped_line: str = line.strip()
            domain: str = stripped_line.split(' ')[1] + '\n'
            return domain
        except IndexError as e:
            self.logger.error(f'line: {line}, {e}')
            return ''

    def _extract_domain_with_regex(self, line: str) -> str:
        """
        Extract domain using regular expression and return it.

        Args:
            line (str): A string representing a line in a file.

        Returns:
            A string representing the extracted domain name.

        """
        match: re.Match[str] | None = self.domain_regex.search(line)
        if not match:
            return ''
        else:
            return match.group() + '\n'

    def extract_domain_from_line(self, line: str) -> str:
        """
        Extract domain if the line matches a regular expression and return it.

        Args:
            line (str): A string representing a line in a file.

        Returns:
            A string representing the extracted domain name.

        """
        if line.startswith(self.localhost_ip):
            return self._extract_domain_if_starts_with_localhost_ip(line)

        elif line.startswith(self.non_routable_ip):
            return self._extract_domain_if_starts_with_non_rout_ip(line)

        else:
            return self._extract_domain_with_regex(line)

    def extract_domain_to_unique_domains_set(self) -> None:
        """
        Extract domains from given the source file and pass them to UniqueDomains
        instance to populate the unique domains set.

        Raises:
            SystemExit: If the source file does not exist.
        """
        whitelist: set[str] = \
            WhitelistSources().get_lines_of_all_sources_contents()

        if not self.file_path.exists():
            self.logger.error(f'{self.file_path} does not exist.')
            raise SystemExit('Operation failed.')

        print('Extracting domains, formatting and removing duplicates...')
        with open(self.file_path, 'r') as raw_hosts:
            for line in raw_hosts:
                if line.startswith(
                        ('#', '<', '\n', '::1')
                ) or line in whitelist:
                    continue
                else:
                    domain: str = self.extract_domain_from_line(line)
                    UniqueBlacklistedDomains().add_domain(domain)
            self.logger.info(f'Extracted domains from {self.file_path}')
