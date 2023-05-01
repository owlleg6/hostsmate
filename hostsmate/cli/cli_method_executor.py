from typing import Callable
from logging import Logger
from json import JSONDecodeError

from hostsmate.autorunner import Autorunner
from hostsmate.suspender import Suspender
from hostsmate.logger import HostsLogger
from hostsmate.system_hosts_file import SystemHostsFile
from hostsmate.sources.whitelist_sources import WhitelistSources
from hostsmate.sources.blacklist_sources import BlacklistSources


class CLIMethodExecutor:
    """
    A class responsible for executing a method based on parsed command-line arguments.

    Attributes:
        flag_method_map (dict): A mapping of command-line arguments to their corresponding methods.
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    flag_method_map: dict[str, Callable] = {
        'go': SystemHostsFile().update_with_new_domains,
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
    ) -> Callable:
        """
        Executes the method based on the given command-line argument and its value.

        Args:
            cli_arg (tuple): A tuple containing the command-line argument and its value.
        """
        arg, value = cli_arg
        self.logger.info(f'CLI args passed: {arg, value}')

        try:
            if type(value) == str:
                self.logger.info(f'Starting method: {self.flag_method_map[arg]}'
                                 f'with args {value}')
                self.flag_method_map[arg](value)
            else:
                self.logger.info(f'Starting method: {self.flag_method_map[arg]}')
                self.flag_method_map[arg]()
                return self.flag_method_map[arg]

        except OSError as e:
            print(f'Operation failed: {e}')
        except JSONDecodeError as e:
            print(f'Operation failed: {e}')