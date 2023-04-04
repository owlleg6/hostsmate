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

    Attributes:
        temp_file (str) path to temporary file for RawHostsCollector and
        Formatter classes usage.
    """
    temp_file: str = OSUtils().mk_tmp_hex_file()

    def run(self) -> None:
        """
        Collects domain entries from raw sources, formats them, removes
        duplicates, and writes the resulting entries to the hosts file.
        """
        RawHostsCollector().process_sources_concurrently(self.temp_file)
        Formatter().format_raw_lines(self.temp_file)
        UniqueDomains().get_unique_domains()
        Writer().build_hosts_file()
