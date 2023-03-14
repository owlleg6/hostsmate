from khostman.logger.logger import logger
from khostman.utils.utils import get_platform

import pathlib
import sys


class Suspender:
    def __init__(self):
        self.platform = get_platform()
        self.darwin = self.platform.startswith('linux') \
                      or self.platform.startswith('darwin') \
                      or self.platform.startswith('freebsd')

        self.windows = self.platform.startswith('win')
        self.darwin_org_hosts_name = pathlib.Path('/etc/hosts')
        self.darwin_renamed_hosts = pathlib.Path('/etc/hosts~')

    def suspend(self) -> None:
        """
        Suspend the adblocking for corresponding platforms
        """
        if self.darwin:
            self.darwin_suspender()
        elif self.windows:
            self.windows_suspender()

    def resume(self) -> None:
        """
        Resume the adblocking for corresponding platforms
        """
        if self.darwin:
            self.darwin_resumer()
        elif self.windows:
            self.windows_resumer()

    def darwin_suspender(self) -> None:
        """
        Suspend the adblocking for Linux, MacOSor FreeBSD
        """

        if self.darwin_renamed_hosts.exists():
            logger.debug(f'{self.darwin_renamed_hosts} already exists. Exiting')
            exit('Adblocking already suspended')
        try:
            self.darwin_org_hosts_name.rename(
                                        self.darwin_renamed_hosts)
            print("Adblocking is being suspended. Don't forget to enable it back!")
            logger.debug(f'Adblocking has been suspended. "{self.darwin_org_hosts_name}" renamed to "{self.darwin_renamed_hosts}"')
        except FileNotFoundError:
            logger.debug('Hosts file in /etc was not found. Exiting')
            exit('Hosts file in /etc was not found.')

    @staticmethod
    def windows_suspender() -> None:
        """
        Suspend the adblocking for Windows
        """
        root_drive = pathlib.Path(sys.executable).anchor
        hosts = pathlib.Path(root_drive + r'Windows\System32\drivers\etc\hosts')
        renamed_hosts = pathlib.Path(root_drive + r'Windows\System32\drivers\etc\hosts~')

        if renamed_hosts.exists():
            logger.debug(f'{renamed_hosts} already exists. Exiting')
            exit('Adblocking already suspended')
        try:
            hosts.rename('hosts~')
            logger.debug('Adblocking has been suspended. '
                         r'"Windows\System32\drivers\etc\hosts" renamed to '
                         r'"Windows\System32\drivers\etc\hosts~"')
        except FileNotFoundError:
            logger.debug(f'Hosts file in was not found in {hosts}')
            exit(r'Hosts file in was not found in Windows\System32\drivers\etc\hosts')

    def darwin_resumer(self) -> None:
        """
        Resume the adblocking for Linux, MacOSor FreeBSD
        """
        try:
            self.darwin_renamed_hosts.rename(self.darwin_org_hosts_name)
            print('Adblocker has been resumed')
            logger.debug('Adblocker has been resumed')
        except FileNotFoundError:
            logger.debug(f'No {self.darwin_renamed_hosts} file was found')
            exit('Seems that the adblocker is running already.')

    @staticmethod
    def windows_resumer() -> None:
        """
        Resume the adblocking for Windows
        """
        root_drive = pathlib.Path(sys.executable).anchor
        renamed_hosts = pathlib.Path(root_drive + r'Windows\System32\drivers\etc\hosts~')
        try:
            renamed_hosts.rename('hosts')
            logger.debug('Adblocker has been resumed. '
                         r'"Windows\System32\drivers\etc\hosts" renamed to '
                         r'"Windows\System32\drivers\etc\hosts~"')
        except FileNotFoundError:
            logger.debug(r'Windows\System32\drivers\etc\hosts~ was not found')
            exit('Seems that the adblocker is running already.')
