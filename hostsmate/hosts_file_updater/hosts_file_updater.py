from hostsmate.formatter.formatter import Formatter
from hostsmate.raw_hosts_collector.raw_hosts_collector import RawHostsCollector
from hostsmate.unique_domains.unique_domains import UniqueDomains
from hostsmate.utils.os_utils import OSUtils
from hostsmate.writer.writer import Writer


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

        RawHostsCollector().process_sources_concurrently(temp_file)
        Formatter().format_raw_lines(temp_file)
        Writer().build_hosts_file()
