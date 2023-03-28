from os import remove
import concurrent.futures
from typing import Optional
from requests import get, RequestException


from khostman.logger.logger import logger
from khostman.utils.data_utils import DataUtils
from khostman.utils.logging_utils import LoggingUtils


class RawHostsCollector:
    """A class for extracting raw contents from blacklist sources and storing them in a temporary file.
       This needed for cleaning and formatting the data by Formatter class


    Attributes:
        blacklist_sources (list): A list of URLs containing blacklisted domains.

    Methods:
        __init__(): Initializes an instance of the class.
        get_hosts_from_source(url, tmp): Downloads domains from a given source URL and writes them to a temporary file.
        extract_raw_sources_contents(tmp): Extracts raw contents from blacklist sources and whitelist and stores them in a
            temporary file.

    """

    @LoggingUtils.func_and_args_logging
    def __init__(self):
        self.blacklist_sources = DataUtils.extract_sources_from_json(blacklist=True)

    @staticmethod
    @LoggingUtils.func_and_args_logging
    def fetch_source_contents(url: str) -> Optional[str]:
        """Fetch source contents and return it as a string.

        Args:
            url (str): the URL containing list of blacklisted domains.

        Returns:
            A string with the complete source contents.
            If an error occurs while fetching the contents, None is returned.
        """
        try:
            print(f'Fetching blacklisted domains from {url}')
            response = get(url)
            response.raise_for_status()
            contents = response.text
            return contents
        except RequestException as e:
            logger.error(f'Could not fetch blacklisted domains from {url}: {e}')
            print(f'Could not fetch blacklisted domains from {url}')
            return None

    @LoggingUtils.func_and_args_logging
    def get_hosts_from_source(self, url, temp_file):
        """ 
        Gets the domains from a given source URL, and writes them to a temporary file 
        """
        contents = self.fetch_source_contents(url)
        if contents is not None:
            with open(temp_file, 'a') as f:
                f.write(f'{contents}\n')

    @LoggingUtils.func_and_args_logging
    def extract_raw_sources_contents(self, tmp: str):
        """
        Extracts raw contents from blacklist sources and whitelist, and stores them in a temporary file.

        :param tmp: path to temporary file
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # iterate through blacklist sources and fetch hosts in parallel
            for source in self.blacklist_sources:
                executor.submit(self.get_hosts_from_source, source, tmp)

    def __repr__(self):
        return f'{__class__.__name__}'
