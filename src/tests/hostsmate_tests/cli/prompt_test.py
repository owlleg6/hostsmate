import pytest
from typing import Union

from hostsmate_src.cli.prompt import Prompt

Fixture = Union


@pytest.fixture
def test_ask_autorun_frequency_setup(
        monkeypatch: pytest.MonkeyPatch,
        input_: str
):
    monkeypatch.setattr('builtins.input', lambda _: input_)


@pytest.mark.parametrize('input_', ['1', '2', '3'])
def test_ask_autorun_frequency_valid_input(
        test_ask_autorun_frequency_setup: Fixture,  # type: ignore
        input_: str
):
    assert Prompt().ask_autorun_frequency() == input_


@pytest.mark.parametrize('input_', ['q', 'Q'])
def test_ask_autorun_frequency_quit(
        test_ask_autorun_frequency_setup: Fixture,  # type: ignore
        input_: str
):
    with pytest.raises(SystemExit):
        Prompt().ask_autorun_frequency()


@pytest.mark.parametrize('input_', ['invalid', 'input'])
def test_ask_autorun_invalid_input(
        test_ask_autorun_frequency_setup: Fixture,  # type: ignore
        input_: str,
        capsys: Fixture  # type: ignore
):
    with pytest.raises(SystemExit):
        Prompt().ask_autorun_frequency()
