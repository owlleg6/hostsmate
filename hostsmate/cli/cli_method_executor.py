from typing import Callable
from logging import Logger

from hostsmate.autorunner import Autorunner
from hostsmate.hosts_file_updater import HostsFileUpdater
from hostsmate.suspender import Suspender
from hostsmate.writer import Writer
from hostsmate.logger import HostsLogger


class CLIMethodExecutor:
    """
    A class responsible for executing a method based on parsed command-line arguments.

    Attributes:
        flag_method_map (dict): A mapping of command-line arguments to their corresponding methods.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    flag_method_map: dict[str, Callable] = {
        'go': HostsFileUpdater.run,
        'autorun': Autorunner().set_anacron_job,
        'backup': Writer().create_backup,
        'suspend': Suspender().suspend,
        'resume': Suspender().resume,
        'blacklist_domain': Writer().block_domain,
        'whitelist_domain': Writer().whitelist_domain,
    }

    def execute(
            self,
            cli_arg:
            tuple[str, str | bool]
    ) -> Callable:
        """
        Executes the method based on the given command-line argument and its value.

        Args:
            cli_arg (tuple): A tuple containing the command-line argument and its value.
        """
        arg, value = cli_arg
        self.logger.info(f'CLI args passed: {arg, value}')

        if type(value) == str:
            self.logger.info(f'Starting method: {self.flag_method_map[arg]}'
                             f'with args {value}')
            self.flag_method_map[arg](value)
        else:
            self.logger.info(f'Starting method: {self.flag_method_map[arg]}')
            self.flag_method_map[arg]()

        return self.flag_method_map[arg]
