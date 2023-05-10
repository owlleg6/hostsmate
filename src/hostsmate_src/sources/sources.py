import concurrent.futures
import json
from abc import ABC, abstractmethod
from io import StringIO
from pathlib import Path

from requests import get, Response, RequestException

from hostsmate_src.logger import HostsLogger


class Sources(ABC):
    """
    Abstract class representing sources of blacklisted and whitelisted domains.
    """

    logger = HostsLogger().create_logger('Sources')

    @property
    @abstractmethod
    def sources_json_path(self) -> Path:
        """Return an absolute path to the JSON file containing source URLs

        Returns:
            Path: An absolute path to the JSON file containing source URLs.
        """
        pass

    @property
    def sources_urls(self) -> set[str]:
        """
        Returns a set of URLs for the sources specified in a JSON file.

        Returns:
            A set of strings representing URLs for the sources specified
            in a JSON resources file.
        """
        with open(self.sources_json_path) as source:
            json_contents: dict[str, list[str]] = json.load(source)
            sources_urls: set[str] = set(json_contents['sources'])
            return sources_urls

    def add_url_to_sources(self, new_source) -> None:
        """Add specified URL to the sources JSON file.

        Args:
            new_source (str): The new URL to add to the sources JSON file.

        Raises:
            SystemExit: if OSError, JSONDecodeError raised or new_source
            is already present in sources.
        """
        if new_source in self.sources_urls:
            raise SystemExit('Source is already in the list.')
        try:
            with open(self.sources_json_path, 'r') as f:
                data = json.load(f)
            data['sources'].append(new_source)
            with open(self.sources_json_path, 'w') as f:
                json.dump(data, f)
            self.logger.info(f'{new_source} added to {self.sources_json_path}')
        except json.JSONDecodeError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')

    def remove_url_from_sources(self, source_to_remove) -> None:
        """Remove specified URL from the sources JSON file.

        Args:
            source_to_remove (str): The URL to remove from the sources JSON file.

        Raises:
            SystemExit: if OSError, JSONDecodeError raised or source_to_remove
            is not present in sources.
        """
        if source_to_remove not in self.sources_urls:
            raise SystemExit('No such a source to remove.')
        with open(self.sources_json_path, 'r') as f:
            contents = json.load(f)
        if source_to_remove in contents['sources']:
            contents['sources'].remove(source_to_remove)
            with open(self.sources_json_path, 'w') as f:
                json.dump(contents, f)

    def fetch_source_contents(self, url: str) -> str:
        """Fetch source contents and return it as a string.

        Args:
            url (str): the URL containing list of blacklisted domains.

        Returns:
            A string with the complete source contents.
            If RequestException raised while fetching the contents, returns an
            empty string.
        """
        try:
            response: Response = get(url, timeout=5)
            response.raise_for_status()

            contents: str = response.text
            self.logger.info(f'Fetched contents of {url}')
            return contents
        except RequestException as e:
            self.logger.error(f'Could not fetch contents of {url}: {e}')
            print(f'Could not fetch blacklisted domains from {url}')
            return ''

    def append_source_contents_to_file(
            self,
            url: str,
            file: str | Path
    ) -> None:
        """Append contents of the given URL to the temporary file.
           Get the source contents by calling fetch_source_contents method

        Args:
             url (str): the URL containing list of blacklisted domains.
             file (str): path to the temporary file
        """
        contents: str = self.fetch_source_contents(url)

        if not contents:
            return

        with open(file, 'a') as f:
            f.write(f'{contents}\n')

    def append_sources_contents_to_file_concurrently(
            self,
            file: str | Path
    ) -> int:
        """Fetch raw contents from all sources and write them concurrently to
        a file with the process pool executor.


        Args:
            file (str): The path to the temporary file where the extracted
            contents will be written.

        Returns
            futures_completed (int): how many processes completed.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures_completed = 0
            futures = []
            for source in self.sources_urls:
                future: concurrent.futures.Future = executor.submit(
                    self.append_source_contents_to_file,
                    source,
                    file
                )
                futures.append(future)

            for _ in concurrent.futures.as_completed(futures):
                futures_completed += 1

        return futures_completed

    def get_lines_of_all_sources_contents(self) -> set[str]:
        """Return each line from all sources as a set.

        Returns:
            A set of line of all sources.
        """
        sources_lines: set[str] = set()

        for source in self.sources_urls:
            resp: str = self.fetch_source_contents(source)
            buffer: StringIO = StringIO(resp)
            sources_lines.update(buffer.readlines())
        return sources_lines
