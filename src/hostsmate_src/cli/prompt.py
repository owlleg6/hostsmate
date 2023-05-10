from logging import Logger

from hostsmate_src.logger import HostsLogger


class Prompt:
    """A class for prompting the user via the command line interface.

    Methods:
        ask_autorun_frequency() -> str
    """

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    def ask_autorun_frequency(self) -> str:
        """Prompt the user to select the frequency of autorun.

        Returns:
            str: The selected autorun frequency ('1', '2', or '3').

        Raises:
            SystemExit: if the user entered "q"
        """
        wrong_input: str = 'Unrecognized input. Try again.\n'

        freq_map: dict = {
            '1': 'daily',
            '2': 'weekly',
            '3': 'monthly'
        }
        frequency: str = input(
            'How often do you want to autorun HostsMate to update your '
            'Hosts file?\n'
            '(enter 1, 2 or 3)\n'
            '1. Daily\n'
            '2. Weekly\n'
            '3. Monthly\n'
            'Enter "q" to quit.\n'
        )
        if frequency.lower() == 'q':
            raise SystemExit
        if frequency in ['1', '2', '3']:
            self.logger.info(f'Chosen autorun frequency: '
                             f'{freq_map[frequency]}')
            return frequency
        else:
            raise SystemExit(wrong_input)
