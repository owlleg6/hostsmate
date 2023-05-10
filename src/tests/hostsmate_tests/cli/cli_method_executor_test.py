import pytest
from unittest.mock import Mock
from json import JSONDecodeError

from hostsmate_src.cli.cli_method_executor import CLIMethodExecutor


method_mock: Mock = Mock()
method_with_args: Mock = method_mock.method_with_args
method_without_args: Mock = method_mock.method_without_args


def method_raises_os_err() -> None:
    raise OSError('Permission denied.')


def method_raises_json_decode_err() -> None:
    raise JSONDecodeError('Cannot resolve character', 'dummy.json', 12)


@pytest.fixture
def dummy_flag_method_map_setup(
        monkeypatch: pytest.MonkeyPatch
):
    dummy_flag_method_map: dict = {
        'method_with_args': method_with_args,
        'method_without_args': method_without_args,
        'method_raises_os_err': method_raises_os_err,
        'method_raises_json_decode_err': method_raises_json_decode_err
    }
    monkeypatch.setattr(
        CLIMethodExecutor, 'flag_method_map',
        dummy_flag_method_map
    )


def test_all_cli_options_present_in_args_map():
    available_cli_options: list[str] = [
        'run',
        'autorun',
        'backup',
        'suspend',
        'resume',
        'blacklist_domain',
        'whitelist_domain',
        'add_whitelist_source',
        'add_blacklist_source',
        'remove_whitelist_source',
        'remove_blacklist_source'
    ]

    flag_map_keys = CLIMethodExecutor.flag_method_map.keys()
    assert all(cli_option in flag_map_keys for cli_option in available_cli_options)


def test_execute_method_no_args(dummy_flag_method_map_setup):
    CLIMethodExecutor().execute(
        ('method_without_args', True)
    )
    method_without_args.assert_called()


def test_execute_method_with_args(dummy_flag_method_map_setup):
    CLIMethodExecutor().execute(
        ('method_with_args', 'FooBar')
    )
    method_with_args.assert_called_with('FooBar')


def test_execute_method_raises_os_error(
        dummy_flag_method_map_setup,
        capsys
):
    CLIMethodExecutor().execute(
        ('method_raises_os_err', True)
    )
    assert capsys.readouterr().out == 'Operation failed: Permission denied.\n'


def test_method_raises_json_decode_err(
        dummy_flag_method_map_setup,
        capsys
):
    CLIMethodExecutor().execute(
        ('method_raises_json_decode_err', True)
    )
    assert capsys.readouterr().out == \
           'Operation failed: Cannot resolve character: ' \
           'line 1 column 13 (char 12)\n'
