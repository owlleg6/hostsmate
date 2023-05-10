from typing import Callable
from logging import Logger
from json import JSONDecodeError

from hostsmate_src.autorunner import Autorunner
from hostsmate_src.suspender import Suspender
from hostsmate_src.logger import HostsLogger
from hostsmate_src.system_hosts_file import SystemHostsFile
from hostsmate_src.sources.whitelist_sources import WhitelistSources
from hostsmate_src.sources.blacklist_sources import BlacklistSources


class CLIMethodExecutor:
    """
    A class responsible for executing a method based on parsed command-line
     arguments.

    Attributes:
        flag_method_map (dict): A mapping of command-line arguments to their
        corresponding methods.

    Methods:
        execute(cli_arg: tuple[str, str | bool]) -> None: Execute the method
        based on the given command-line argument and its value.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    flag_method_map: dict[str, Callable] = {
        'run': SystemHostsFile().update_with_new_domains,
        'autorun': Autorunner().set_up_anacron_job,
        'backup': SystemHostsFile().create_backup,
        'suspend': Suspender().suspend,
        'resume': Suspender().resume,
        'blacklist_domain': SystemHostsFile().add_blacklisted_domain,
        'whitelist_domain': SystemHostsFile().remove_domain,
        'add_whitelist_source': WhitelistSources().add_url_to_sources,
        'add_blacklist_source': BlacklistSources().add_url_to_sources,
        'remove_whitelist_source': WhitelistSources().remove_url_from_sources,
        'remove_blacklist_source': BlacklistSources().remove_url_from_sources
    }

    def execute(
            self,
            cli_arg:
            tuple[str, str | bool]
    ) -> None:
        """
        Execute the method based on the given command-line argument and its value.

        Args:
            cli_arg (tuple): A tuple containing the command-line argument and its value.
        """
        arg, value = cli_arg
        self.logger.info(f'CLI args passed: {arg, value}')

        try:
            if isinstance(value, str):
                self.logger.info(f'Starting method: {self.flag_method_map[arg]}'
                                 f'with args {value}')
                self.flag_method_map[arg](value)
            else:
                self.logger.info(f'Starting method: {self.flag_method_map[arg]}')
                self.flag_method_map[arg]()

        except OSError as e:
            print(f'Operation failed: {e}')
            self.logger.error(f'Operation failed: {e}')
        except JSONDecodeError as e:
            print(f'Operation failed: {e}')
            self.logger.error(f'Operation failed: {e}')
