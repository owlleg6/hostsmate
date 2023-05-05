import argparse
import sys
from logging import Logger

from src.hostsmate.logger import HostsLogger


class Parser:
    """This class provides a command-line user interface for managing
     the application.

    It uses argparse module to define a set of cli options,
    parse arguments given to the application and run corresponding methods.
    """

    def __init__(self):
        """Initialize the Parser object by ensuring that the user has root
        privileges, creating an ArgumentParser object with predefined
        arguments, and parsing the command-line arguments. Print help
        message if no arguments were provided.
        """
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)
        self.parser: argparse.ArgumentParser = self.create_parser()
        self.help_if_no_args()
        self.args_: dict[str, str | bool] = vars(self.parser.parse_args())

    def create_parser(self) -> argparse.ArgumentParser:
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
            description='Welcome to HostsMate! A system-wide ad blocker by Kravchenkoda. '
                        'Protect yourself from malware, tracking, ads and spam.\n'
                        'HostsMate blacklists 1.4 million+ domains from 44 sources '
                        'that update regularly to keep your system safe.\n\n'
                        'GitHub repository: https://github.com/kravchenkoda/hostsmate',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            '-g',
            '--go',
            action='store_true',
            help='Parse domains from blacklist sources and start the HostsMate.'
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
            help="Suspend HostsMate. Don't forget to turn it back!")
        group.add_argument(
            '-r',
            '--resume',
            action='store_true',
            help='Resume HostsMate after suspension.'
        )
        group.add_argument(
            '-b',
            '--backup',
            type=str,
            metavar='[backup-path]',
            help='Create a backup of the existing Hosts '
                 'file in the specific folder.'
        )
        group.add_argument(
            '-x',
            '--blacklist-domain',
            type=str,
            metavar='[domain]',
            help='Blacklist specified domain.'
        )
        group.add_argument(
            '-w',
            '--whitelist-domain',
            metavar='[domain]',
            type=str,
            help='Whitelist specified domain.')

        group.add_argument(
            '-y',
            '--add-whitelist-source',
            metavar='[domain]',
            type=str,
            help='Add URL with whitelisted domains to whitelist sources.')

        group.add_argument(
            '-u',
            '--add-blacklist-source',
            metavar='[domain]',
            type=str,
            help='Add URL with blacklisted domains to blakclist sources.')

        group.add_argument(
            '-i',
            '--remove-whitelist-source',
            metavar='[domain]',
            type=str,
            help='Remove URL with whitelisted domains from whitelist sources.')

        group.add_argument(
            '-o',
            '--remove-blacklist-source',
            metavar='[domain]',
            type=str,
            help='Remove URL with blacklisted domains from blacklist sources.')

        self.logger.info('argparse.ArgumentParser instance created.')
        return parser

    def help_if_no_args(self):
        """
        Prints help message and exits if ran with no arguments.

        Raises:
            SystemExit
        """
        if len(sys.argv) == 1:
            self.parser.print_help()
            self.logger.info('Ran with no arguments. Printed help')
            raise SystemExit

    def parse_single_arg(self) -> tuple[str, str | bool]:
        """
        Parse the argument and its value.

        Returns:
             tuple containing argument and its value.
        """
        for arg, value in self.args_.items():
            if value:
                return arg, value

    def __repr__(self):
        return f'{__class__.__name__}(args_:{self.args_})'
