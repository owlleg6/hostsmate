from khostman.logger.logger import logger
from khostman.utils.os_utils import OSUtils


class Suspender:
    """
    A class for suspending and resuming an adblocker by renaming the hosts file.
    """

    org_hosts_name = OSUtils().path_to_hosts()

    renamed_hosts = org_hosts_name.with_name(org_hosts_name.name + '~')

    def suspend(self) -> None:
        """
        Suspend the adblocking
        """
        try:
            self.org_hosts_name.rename(
                self.renamed_hosts)
            print("Adblocking is being suspended. Don't forget to enable it back!")
            logger.debug(f'Adblocking has been suspended. "{self.org_hosts_name}" renamed to "{self.renamed_hosts}"')
        except FileNotFoundError:
            logger.debug(f'Hosts file {self.org_hosts_name} was not found. Exiting')
            exit(f'Hosts file {self.org_hosts_name} was not found.')

    def resume(self) -> None:
        """
        Resume the adblocking
        """
        try:
            self.renamed_hosts.rename(self.org_hosts_name)
            print('Adblocker has been resumed')
            logger.debug('Adblocker has been resumed')
        except FileNotFoundError:
            logger.debug(f'No {self.renamed_hosts} file was found')
            exit('Seems that the adblocker is running already.')
