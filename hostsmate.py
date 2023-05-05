from src.hostsmate.cli.parser import Parser
from src.hostsmate.cli.cli_method_executor import CLIMethodExecutor


def main() -> None:
    """Parse the command-line argument and execute the corresponding method."""
    cli_args_parser: Parser = Parser()
    cli_arg: tuple[str, str | bool] = cli_args_parser.parse_single_arg()
    CLIMethodExecutor().execute(cli_arg)


if __name__ == '__main__':
    main()
