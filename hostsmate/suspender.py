from pathlib import Path
from logging import Logger

from hostsmate.logger import HostsLogger
from hostsmate.utils.os_utils import OSUtils


class Suspender:
    """
    A class for suspending and resuming an adblocker by renaming the system's Hosts file.

    Attributes:
        org_hosts_name (Path): a path to the system's Hosts file.
        renamed_hosts (Path): a path the renamed system's Hosts file (with tilda).
    """

    org_hosts_name: Path = OSUtils().path_to_hosts()
    renamed_hosts: Path = org_hosts_name.with_name(org_hosts_name.name + '~')

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def suspend(self) -> None:
        """
        Suspend the adblocking by renaming the Hosts file.
        """
        try:
            self.org_hosts_name.rename(
                self.renamed_hosts)
            print("Adblocking is being suspended. Don't forget to enable it back!")
            self.logger.info(f'Adblocking has been suspended. "{self.org_hosts_name}" renamed to "{self.renamed_hosts}"')
        except FileNotFoundError:
            self.logger.info(f'Hosts file {self.org_hosts_name} was not found. Exiting')
            exit(f'Hosts file {self.org_hosts_name} was not found.')

    def resume(self) -> None:
        """
        Resume the adblocking by renaming the Hosts file.
        """
        try:
            self.renamed_hosts.rename(self.org_hosts_name)
            print('Adblocker has been resumed')
            self.logger.info('Adblocker has been resumed')
        except FileNotFoundError:
            self.logger.info(f'No {self.renamed_hosts} file was found')
            exit('Seems that the adblocker is running already.')
