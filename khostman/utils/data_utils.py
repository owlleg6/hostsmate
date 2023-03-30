import json
from pathlib import Path

from khostman.utils.utils import Utils
from khostman.utils.os_utils import OSUtils
from khostman.logger.logger import logger


class DataUtils(Utils):
    """A collection of utility methods for data processing."""

    @staticmethod
    def extract_sources_from_json(whitelist=False, blacklist=False) -> list[str]:
        """
        Extracts a list of sources from a JSON file.

        Args:
            whitelist (bool): Return whitelist sources.
            blacklist (bool): Return blacklist sources.

        Returns:
            list[str]: A list of sources extracted from the JSON file.
        """
        resources_dir: Path = OSUtils.get_project_root() / 'khostman' / 'resources'

        if whitelist:
            source_json: Path = resources_dir / 'whitelist_sources.json'
        elif blacklist:
            source_json: Path = resources_dir / 'blacklist_sources.json'

        else:
            logger.error('No list type (blacklist or whitelist) was specified')
            raise ValueError('"whitelist" or "blacklist" argument must be set to True')

        with open(source_json) as source:
            contents: dict[str, list[str]] = json.load(source)
            sources: list[str] = contents['sources']
            logger.debug(f'Sources from {resources_dir} source were fetched')
            return sources
