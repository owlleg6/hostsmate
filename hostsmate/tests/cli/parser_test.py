import argparse
import sys
from argparse import RawDescriptionHelpFormatter

import pytest

from hostsmate.cli.parser import Parser


def test_create_parser(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, 'argv',
        ['hostsmate.py', '--go']
    )
    parser: argparse.ArgumentParser = Parser().parser

    number_of_available_args: int = \
        len(parser._mutually_exclusive_groups[0]._group_actions)

    assert parser.description.startswith('Welcome to HostsMate!')
    assert parser.formatter_class == RawDescriptionHelpFormatter
    assert number_of_available_args == 11


def test_help_if_no_args(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, 'argv',
        ['hostsmate.py']
    )

    with pytest.raises(SystemExit):
        Parser()


def test_parse_single_arg(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, 'argv',
        ['hostsmate.py', '--go']
    )

    assert Parser().parse_single_arg() == ('go', True)

