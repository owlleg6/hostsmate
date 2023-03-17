import pathlib
from os import remove
from typing import Set
from requests import get
from urllib.parse import urlparse
from io import StringIO
import re

from khostman.utils.logging_utils import LoggingUtils
from khostman.logger.logger import logger
from khostman.sources.sources import Sources


class Formatter:
    localhost = '127.0.0.1'
    void_id = '0.0.0.0'
    domain_regex = re.compile('([a-z0-9-]+[.]+)+[a-z0-9-]+')

    def __init__(self):
        self.unique_domains = set()
        self.whitelist = self.get_whitelist()

    @staticmethod
    def get_whitelist():
        whitelist = set()
        for whitelist_source in Sources().whitelist_sources:
            resp = get(whitelist_source).text
            buffer = StringIO(resp)
            whitelist.update(buffer.readlines())
        return whitelist

    def extract_domain(self, line: str) -> str:
        """Extract domain from the given string(line)"""
        try:
            if line.startswith(self.localhost):
                line = line.strip()
                return line.split(' ')[1] + '\n'

            elif line.startswith(self.void_id):
                line = line.strip()
                return ' '.join(line.split(' ')[:2]) + '\n'
            else:
                match = self.domain_regex.search(line)
                if match:
                    return match.group() + '\n'
        except IndexError:
            logger.debug(line)

    def remove_duplicates(self, domain: str) -> None:
        """Add a domain to the unique_domains set"""
        if domain is None:
            return
        if domain.startswith('0.0.0.0'):
            self.unique_domains.add(domain)
        else:
            self.unique_domains.add(f'0.0.0.0 {domain}')

    @LoggingUtils.timer
    def get_unique_domains(self, contents: str) -> Set[str]:
        print('Extracting domains, formatting and removing duplicates...')
        if not pathlib.Path(contents).exists():
            exit('Please check your internet connection and try again.')
        with open(contents, 'r') as raw_hosts:
            for line in raw_hosts:
                if line.startswith(('#', '<', '\n')) \
                        or ('::1' in line) \
                        or line in self.whitelist:
                    continue
                else:
                    domain = self.extract_domain(line)
                    self.remove_duplicates(domain)
        logger.info('unique_domains set was created. Temporary file was removed.')
        return self.unique_domains

    @staticmethod
    def strip_domain_prefix(url):
        """
        Given a URL string, returns the domain name with any leading "www." prefix removed.

        Parameters:
            url (str): The URL string to strip.

        Returns:
            str: The stripped domain name.

        Example:
            >>> strip_domain_prefix('http://www.example.com')
            'example.com'
        """
        if urlparse(url).scheme:
            domain = urlparse(url).netloc.split(':')[0]
            if domain.startswith('www.'):
                return domain[4:]
            return domain
        else:
            domain = urlparse(url).path
            if domain.startswith('www.'):
                return domain[4:]
            return url
