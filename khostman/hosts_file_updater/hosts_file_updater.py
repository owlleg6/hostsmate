from khostman.formatter.formatter import Formatter
from khostman.raw_hosts_collector.raw_hosts_collector import RawHostsCollector
from khostman.unique_domains.unique_domains import UniqueDomains
from khostman.utils.os_utils import OSUtils
from khostman.writer.writer import Writer


class HostsFileUpdater:
    """
    Managing class that updates the system hosts file by downloading raw sources of
    domain entries, formatting them, removing duplicates, and writing the
    resulting entries, along with the header, to the hosts file.
    """
    tmp = OSUtils.mk_tmp_hex_file()

    def run(self) -> None:
        """
        Collects domain entries from raw sources, formats them, removes
        duplicates, and writes the resulting entries to the hosts file.
        """
        RawHostsCollector().extract_raw_sources_contents(self.tmp)
        Formatter().format_raw_lines(self.tmp)
        UniqueDomains().get_unique_domains()
        Writer().write_to_hosts()
