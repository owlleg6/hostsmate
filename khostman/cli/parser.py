import argparse

from khostman.writer.writer import Writer
from khostman.suspender.suspender import Suspender
from khostman.utils.os_utils import OSUtils
from khostman.utils.logging_utils import LoggingUtils
from khostman.autorunner.autorunner import Autorunner


class Parser:
    flag_map = {
        'autorun': Autorunner().set_anacron_job,
        'backup': Writer().create_backup,
        'suspend': Suspender().suspend,
        'resume': Suspender().resume,
        'blacklist_domain': Writer().block_domain,
        'whitelist_domain': Writer().whitelist_domain,
    }

    def __init__(self):
        OSUtils.ensure_root_privileges()
        self.parser = self.create_parser()
        self.args_ = vars(self.parser.parse_args())

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description='Welcome to the system-wide ad blocker by Kravchenkoda.\n'
                        'Protect yourself from malware, tracking, ads and spam.\n'
                        '1 400 000+ malicious domains from almost 50 sources that update regularly.',
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-g', '--go',
                           action='store_true',
                           help='Parse domains from blacklist sources and start the adblocker.')
        group.add_argument('-a', '--autorun',
                           action='store_true',
                           help='Setup automatic update of your Hosts file (Linux only)')
        group.add_argument('-s', '--suspend',
                           action='store_true',
                           help="Suspend the adblocker. Don't forget to turn it back!")
        group.add_argument('-r', '--resume',
                           action='store_true',
                           help='Resume the adblocker after suspension.')
        group.add_argument('-b', '--backup',
                           action='store_true',
                           help='Create a backup of the existing Hosts file in the specific folder.')
        group.add_argument('-x', '--blacklist_domain',
                           type=str,
                           help='Blacklist specified domain.')
        group.add_argument('-w', '--whitelist_domain',
                           type=str,
                           help='Whitelist specified domain.')

        return parser

    def help(self):
        self.parser.print_help()

    @LoggingUtils.func_and_args_logging
    def parse_arg(self) -> tuple:
        """
        Parse the argument and its value
        :return tuple containing argument and its value
        """
        for arg, value in self.args_.items():
            if value:
                return arg, value

    @LoggingUtils.func_and_args_logging
    def run_method(self, parsed_arg: tuple) -> None:
        """
        Run the method based on the parsed argument
        """
        arg, value = parsed_arg

        if type(value) == str:
            self.flag_map[arg](value)
        else:
            self.flag_map[arg]()

    def __repr__(self):
        return f'{__class__.__name__}(args_:{self.args_})'
