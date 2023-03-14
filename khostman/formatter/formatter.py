from functools import lru_cache
import pathlib
from os import remove
from typing import Set
from requests import get
from urllib.parse import urlparse

from khostman.utils.utils import timer
from khostman.logger.logger import logger
from khostman.unformatted_domains.unformatted_domains import UnformattedDomains
import re


class Formatter:
    """
    Formats the UnformattedDomains instance raw file to extract domains
    """
    whitelist = None

    def __init__(self):
        self.unique_domains = set()
        logger.info(f'Initialization of the {__class__.__name__} class instance')
        self.domain_regex = re.compile('([a-z0-9-]+[.]+)+[a-z0-9-]+')
        self.localhost = '127.0.0.1'
        self.void_id = '0.0.0.0'

    @staticmethod
    @timer
    def get_whitelist():
        logger.debug('Getting whitelist')
        resp = get('https://raw.githubusercontent.com/agneevX/whitelist/master/whitelist.txt').text
        with open('tmp', 'w') as f:
            f.write(resp)
        return open('tmp').readlines()

    @staticmethod
    def contains_url(line):
        if line.startswith(('#', '<', '\n')) \
                or ('::1' in line):
            return False

        line = line.split(' ')
        domain_pattern = re.compile('[a-z0-9]+[.]+[a-z0-9]+')
        for word in line:
            if domain_pattern.search(word):
                return True

    def extract_domain(self, line: str) -> str:

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

    def add_domain(self, line: str) -> None:
        """
        Formats the line and adds domain to the unique_domains set

        domain: A line from the tmp unfromatted hosts file
        """
        multiple_word_line = ' ' in line
        void_ip = '0.0.0.0'
        if multiple_word_line:
            words = line.split(' ')
            if line.startswith('127.0.0.1'):
                self.unique_domains.add(
                    f'{void_ip} {words[1]}')

            elif line.startswith(void_ip):
                self.unique_domains.add(
                    ' '.join(words[:2]))
                if len(words) > 2:
                    self.unique_domains.add(
                        f'{void_ip} {" ".join(words[2:])}\n')
            else:
                self.unique_domains.add(
                    f'{void_ip} {words[0]}\n')
        elif '#' not in line:
            self.unique_domains.add(f'{void_ip} {line}')

    def remove_duplicates(self, domain):
        if domain is None:
            return
        if domain.startswith('0.0.0.0'):
            self.unique_domains.add(domain)
        else:
            self.unique_domains.add(f'0.0.0.0 {domain}')

    @timer
    def extract_domains(self, contents: str) -> Set[str]:
        logger.debug('Entered Formatter.extract_domains()')
        print('Extracting domains, formatting and removing duplicates...')
        if not pathlib.Path(contents).exists():
            exit('Please check your internet connection and try again.')
        with open(contents, 'r') as raw_hosts:
            logger.debug('Entered unformatted hosts file')
            for line in raw_hosts:
                # if self.contains_url(line):
                #     self.add_domain(line)
                if line.startswith(('#', '<', '\n')) \
                        or ('::1' in line):
                    continue
                else:
                    domain = self.extract_domain(line)
                    self.remove_duplicates(domain)
        logger.debug('unique_domains set was created. Temporary file was removed.')
        # print(len(unique_domains))
        # remove(contents)
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
