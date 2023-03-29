import argparse
import sys

from khostman.writer.writer import Writer
from khostman.suspender.suspender import Suspender
from khostman.utils.os_utils import OSUtils
from khostman.utils.logging_utils import LoggingUtils
from khostman.autorunner.autorunner import Autorunner
from khostman.hosts_file_updater.hosts_file_updater import HostsFileUpdater


class Parser:
    """This class provides a command-line user interface for managing
     the application.

    It uses argparse module to define a set of cli options,
    parse arguments given to the application and run corresponding methods.

    Attributes:
        flag_map (dict): A dictionary that maps each command-line option to a
        corresponding method in the HostsFileUpdater, Autorunner, Writer,
        or Suspender class.
    """

    flag_map: dict[str, callable] = {
        'go': HostsFileUpdater().run,
        'autorun': Autorunner().set_anacron_job,
        'backup': Writer().create_backup,
        'suspend': Suspender().suspend,
        'resume': Suspender().resume,
        'blacklist_domain': Writer().block_domain,
        'whitelist_domain': Writer().whitelist_domain,
    }

    def __init__(self):
        """Initialize the Parser object by ensuring that the user has root
        privileges, creating an ArgumentParser object with predefined
        arguments, and parsing the command-line arguments. Print help
        message if no arguments were provided.
        """
        OSUtils.ensure_root_privileges()
        self.parser: argparse.ArgumentParser = self.create_parser()
        self.help_if_no_args()
        self.args_: dict[str, [str | bool]] = vars(self.parser.parse_args())

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        Creates an ArgumentParser object with predefined arguments for the
        command-line user interface. The predefined arguments include options
        to start, suspend, or resume the adblocker, create a backup of the
        existing Hosts file, blacklist or whitelist specified domains, and set
        up automatic updates for the Hosts file.

        Returns:
            argparse.ArgumentParser: An ArgumentParser object with the
            predefined arguments.
        """
        parser = argparse.ArgumentParser(
            description='Welcome to Khostman! A system-wide ad blocker by Kravchenkoda. '
                        'Protect yourself from malware, tracking, ads and spam.\n'
                        'Khostman blacklists 1.4 million+ domains from 44 sources '
                        'that update regularly to keep your system safer.\n\n'
                        'GitHub repository: https://github.com/kravchenkoda/khostman',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            '-g',
            '--go',
            action='store_true',
            help='Parse domains from blacklist sources and start the adblocker.'
        )
        group.add_argument(
            '-a',
            '--autorun',
            action='store_true',
            help='Setup automatic update of your Hosts file (Linux only)'
        )
        group.add_argument(
            '-s',
            '--suspend',
            action='store_true',
            help="Suspend the adblocker. Don't forget to turn it back!")
        group.add_argument(
            '-r',
            '--resume',
            action='store_true',
            help='Resume the adblocker after suspension.'
        )
        group.add_argument(
            '-b',
            '--backup',
            action='store_true',
            help='Create a backup of the existing Hosts '
                 'file in the specific folder.'
        )
        group.add_argument(
            '-x',
            '--blacklist_domain',
            type=str,
            metavar='[domain-to-block]',
            help='Blacklist specified domain.'
        )
        group.add_argument(
            '-w',
            '--whitelist_domain',
            metavar='[domain-to-whitelist]',
            type=str,
            help='Whitelist specified domain.')

        return parser

    def help_if_no_args(self):
        """
        Prints help message and exits if ran with no arguments.
        """
        if len(sys.argv) == 1:
            self.parser.print_help()
            exit()

    @LoggingUtils.func_and_args_logging
    def parse_arg(self) -> tuple[str, [str | bool]]:
        """
        Parse the argument and its value.

        Returns:
             tuple containing argument and its value.
        """
        for arg, value in self.args_.items():
            if value:
                return arg, value

    @LoggingUtils.func_and_args_logging
    def run_method(self, parsed_arg: tuple[str, [str | bool]]) -> None:
        """
        Run the method based on the parsed argument.

        Args:
            parsed_arg (tuple): argument and its value.
        """
        arg, value = parsed_arg

        if type(value) == str:
            self.flag_map[arg](value)
        else:
            self.flag_map[arg]()

    def __repr__(self):
        return f'{__class__.__name__}(args_:{self.args_})'
