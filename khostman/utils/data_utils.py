import json

from khostman.utils.utils import Utils
from khostman.utils.os_utils import OSUtils

class DataUtils(Utils):

    @staticmethod
    def extract_sources_from_json(whitelist=False, blacklist=False) -> list:
        """
        Extracts a list of sources from a JSON file.

        Args:
            whitelist (bool): Return whitelist sources.
            blacklist (bool): Return blacklist sources.

        Returns:
            list: A list of sources extracted from the JSON file.
        """
        resources_dir = OSUtils.get_project_root() / 'khostman' / 'resources'
        if whitelist:
            source_json = resources_dir / 'whitelist_sources.json'
        elif blacklist:
            source_json = resources_dir / 'blacklist_sources.json'

        with open(source_json) as source:
            contents = json.load(source)
            sources = contents['sources']
            return sources