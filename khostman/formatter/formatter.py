from requests import get, RequestException
from urllib.parse import urlparse
from io import StringIO
import re

from khostman.utils.logging_utils import LoggingUtils
from khostman.utils.data_utils import DataUtils
from khostman.logger.logger import logger
from khostman.unique_domains.unique_domains import UniqueDomains


class Formatter:
    """A class for formatting and cleaning the data fetched into temporary file from blacklist domain sources.

    Extract domain names and pass them to UniqueDomains class for unique_domains set creation.

    Attributes:
        localhost (str): localhost ip address.
        void_id (str): non-routable ip address.
        domain_regex (Pattern): regular expression for domain name.
        whitelist_sources (list): a list containing URLs with whitelist sources.
        whitelist (set): a set of whitelisted domain names.
        unique_domains (UniqueDomains): an instance that contains a set of unique blacklisted domain names.

    Methods:
        get_whitelist() -> Set
        extract_domain(line: str) -> str
        remove_duplicates(domain: str) -> None
        format_raw_lines(contents: str) -> None
        strip_domain_prefix(url) -> str
    """
    localhost: str = '127.0.0.1'
    void_id: str = '0.0.0.0'
    domain_regex: re.Pattern = re.compile('([a-z0-9-]+[.]+)+[a-z0-9-]+')
    whitelist_sources: list[str] = DataUtils.extract_sources_from_json(whitelist=True)
    unique_domains = UniqueDomains()

    def __init__(self):
        self.whitelist: set = self.get_whitelist()

    def get_whitelist(self) -> set:
        """Fetches and returns a set of domains from the whitelist sources.

        Returns:
            A set of whitelisted domain names.
        """
        whitelist = set()

        for whitelist_source in self.whitelist_sources:
            try:
                print(f'Fetching whitelisted domains from {whitelist_source}')
                resp: str = get(whitelist_source).text
                buffer: StringIO = StringIO(resp)
                whitelist.update(buffer.readlines())
            except RequestException as e:
                logger.error(f'Error fetching whitelist domains from {whitelist_source}: {e}')
                print(f'Could not fetch whitelist domains from {whitelist_source}')
        return whitelist

    def extract_domain(self, line: str) -> str:
        """Extracts domain from the given input string (line).

        Args:
            line (str): A string containing the domain to be extracted.

        Returns:
            A string containing the extracted domain.
        """
        try:
            if line.startswith(self.localhost):
                line = line.strip()
                return line.split(' ')[1] + '\n'

            elif line.startswith(self.void_id):
                line = line.strip()
                return ' '.join(line.split(' ')[:2]) + '\n'
            else:
                match: re.Match[str] | None = self.domain_regex.search(line)
                if match:
                    return match.group() + '\n'
        except IndexError as e:
            logger.error(f'Error while formatting the line {line}: {e}')

    def remove_duplicates(self, domain: str | None) -> None:
        """Remove duplicates by adding a domain to the unique_domains set.

        Args:
            domain (str): domain name to be added.
        """
        if domain is None:
            return
        if domain.startswith(self.void_id):
            self.unique_domains.add_domain(domain)
        else:
            self.unique_domains.add_domain(f'{self.void_id} {domain}')

    @LoggingUtils.timer
    def format_raw_lines(self, contents: str) -> None:
        """
        Extracts domains from given the source file, formats them, and removes duplicates.

        Args:
            contents: A string representing the path to a file containing raw blacklist sources contents.

        Raises:
            SystemExit: If the file at `contents` does not exist.
        """
        print('Extracting domains, formatting and removing duplicates...')
        with open(contents, 'r') as raw_hosts:
            for line in raw_hosts:
                if line.startswith(('#', '<', '\n')) \
                        or ('::1' in line) \
                        or line in self.whitelist:
                    continue
                else:
                    domain: str = self.extract_domain(line)
                    self.remove_duplicates(domain)

    @staticmethod
    def strip_domain_prefix(url: str) -> str:
        """
        Given a URL string, returns the domain name with any leading protocol or "www." prefix removed.

        Args:
            url (str): The URL string to strip.

        Returns:
            str: The stripped domain name.

        Example:
            >>> strip_domain_prefix('http://www.example.com')
            'example.com'
        """
        if urlparse(url).scheme:
            domain: str = urlparse(url).netloc.split(':')[0]
            if domain.startswith('www.'):
                return domain[4:]
            return domain
        else:
            domain: str = urlparse(url).path
            if domain.startswith('www.'):
                return domain[4:]
            return url
