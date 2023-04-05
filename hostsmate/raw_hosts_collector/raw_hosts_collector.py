import concurrent.futures
from logging import Logger

from requests import get, RequestException, Response

from hostsmate.logger.logger import HostsLogger
from hostsmate.utils.data_utils import DataUtils
from hostsmate.utils.logging_utils import LoggingUtils


class RawHostsCollector:
    """A class for extracting raw contents from blacklist sources and storing them in a temporary file.
       This needed for further cleaning and formatting data to extract unique domains.

    Attributes:
        blacklist_sources (list): A list of URLs containing blacklisted domains.

    Methods:
        fetch_source_contents(url: str) -> Optional[str]
        write_source_to_tmp(url: str, temp_file: str) -> None
        process_sources_concurrently(tmp: str) -> None

    """
    blacklist_sources: list[str] = DataUtils().extract_sources_from_json(blacklist=True)

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def fetch_source_contents(self, url: str) -> str | None:
        """Fetch source contents and return it as a string.

        Args:
            url (str): the URL containing list of blacklisted domains.

        Returns:
            A string with the complete source contents.
            If an error occurs while fetching the contents, None is returned.
        """
        try:
            print(f'Fetching blacklisted domains from {url}')
            response: Response = get(url)
            response.raise_for_status()
            contents: str = response.text
            self.logger.info(f'Fetched contents of {url}')
            return contents
        except RequestException as e:
            self.logger.error(f'Could not fetch contents of {url}: {e}')
            print(f'Could not fetch blacklisted domains from {url}')
            return None

    @LoggingUtils.func_and_args_logging
    def write_source_to_tmp(self, url: str, temp_file: str) -> None:
        """Append contents of the given URL to the temporary file.
           Get the source contents by calling fetch_source_contents method

        Args:
             url (str): the URL containing list of blacklisted domains.
             temp_file (str): path to the temporary file
        """

        contents: str | None = self.fetch_source_contents(url)

        if contents is not None:
            try:
                with open(temp_file, 'a') as f:
                    f.write(f'{contents}\n')
                    self.logger.info(f'Wrote contents of {url} to temp file')
            except OSError as e:
                self.logger.error(f'Failed to write contents of {url} to temp file: {e}')

    @LoggingUtils.func_and_args_logging
    def process_sources_concurrently(self, tmp: str) -> None:
        """Extract raw contents from all blacklist sources and write them to a temporary file.

        This method uses a process pool executor to fetch and write the contents of each blacklist source
        to the same temporary file in parallel.

        Args:
            tmp (str): The path to the temporary file where the extracted contents will be written.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for source in self.blacklist_sources:
                executor.submit(self.write_source_to_tmp, source, tmp)
