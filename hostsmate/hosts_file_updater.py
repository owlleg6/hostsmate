from hostsmate.domains_extractor import DomainsExtractor
from hostsmate.sources.blacklist_sources import BlacklistSources
from hostsmate.utils.os_utils import OSUtils
from hostsmate.system_hosts_file import SystemHostsFile


class HostsFileUpdater:
    """
    Managing class that updates the system Hosts file by downloading raw
    sources of domain entries, formatting them, removing duplicates, and
    writing the resulting entries, along with the header, to the hosts file.
    """

    @staticmethod
    def run() -> None:
        """
        Collects domain entries from raw sources, formats them, removes
        duplicates, and writes the resulting entries to the hosts file.
        """
        temp_file: str = OSUtils().mk_tmp_hex_file()

        BlacklistSources().append_sources_contents_to_file_concurrently(
            temp_file
        )
        DomainsExtractor(temp_file).extract_domain_to_unique_domains_set()
        SystemHostsFile().build()
