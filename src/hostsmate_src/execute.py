from hostsmate_src.cli.parser import Parser
from hostsmate_src.cli.cli_method_executor import CLIMethodExecutor
from hostsmate_src.logger import HostsLogger


def main() -> None:
    """Parse the command-line argument and execute the corresponding method."""
    cli_args_parser: Parser = Parser()
    cli_arg: tuple[str, str | bool] = cli_args_parser.parse_single_arg()
    CLIMethodExecutor().execute(cli_arg)
    print(f'Logs located at: {HostsLogger.get_logs_dir()}')


if __name__ == '__main__':
    main()
