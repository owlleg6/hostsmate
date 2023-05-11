from pathlib import Path
from logging import Logger

from hostsmate_src.logger import HostsLogger
from hostsmate_src.system_hosts_file import SystemHostsFile


class Suspender:
    """
    A class for suspending and resuming an adblocker by renaming the system's
    Hosts file.

    Attributes:
        org_hosts_name (Path): a path to the system's Hosts file.
        renamed_hosts (Path): a path the renamed system's Hosts file (with tilda).

    Methods:
        suspend() -> None
        resume() -> None
    """

    org_hosts_name: Path = SystemHostsFile().original_path
    renamed_hosts: Path = SystemHostsFile().renamed_path

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def suspend(self) -> None:
        """
        Suspend the adblocking by renaming the Hosts file.

        Raises:
            SystemExit: if the hosts file has not been found.
        """
        try:
            self.org_hosts_name.rename(
                self.renamed_hosts)
            print("HostsMate is being suspended. Don't forget to enable it back!")
            self.logger.info(f'HostsMate has been suspended.'
                             f'"{self.org_hosts_name}" renamed to'
                             f'"{self.renamed_hosts}"')
        except FileNotFoundError:
            self.logger.info(f'Hosts file {self.org_hosts_name} has not been found')
            raise SystemExit(f'Hosts file {self.org_hosts_name} has not been found.')

    def resume(self) -> None:
        """
        Resume the adblocking by renaming the Hosts file.

        Raises:
            SystemExit: if the hosts file has not been found.
        """
        try:
            self.renamed_hosts.rename(self.org_hosts_name)
            print('HostsMate has been resumed.')
            self.logger.info('HostsMate has been resumed.')
        except FileNotFoundError:
            self.logger.info(f'No {self.renamed_hosts} has been found')
            raise SystemExit('HostsMate is running already.')
