import pytest
from typing import Union

from hostsmate_src.sources.sources import Sources
from hostsmate_src.sources.whitelist_sources import WhitelistSources

Fixture = Union


class TestWhitelistSources:
    sample_source_url = 'https://foobarzar.com/hosts.txt'

    @staticmethod
    @pytest.fixture
    def instance():
        return WhitelistSources()

    @staticmethod
    def test_sources_json_path(instance: Fixture[WhitelistSources]):  # type: ignore
        assert instance.sources_json_path.exists()  # type: ignore
        assert instance.sources_json_path.parent.name == 'resources'  # type: ignore
        assert instance.sources_json_path.name == 'whitelist_sources.json'  # type: ignore

    def test_add_url_to_sources(
            self,
            instance: Fixture[WhitelistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'add_url_to_sources',
            lambda foo, bar: None
        )

        instance.add_url_to_sources(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'"{self.sample_source_url}" ' \
                         f'has been added to whitelist sources.\n'

    def test_remove_url_from_sources(
            self,
            instance: Fixture[WhitelistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'remove_url_from_sources',
            lambda foo, bar: None
        )

        instance.remove_url_from_sources(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'"{self.sample_source_url}" ' \
                         f'has been removed from whitelist sources.\n'

    def test_fetch_source_contents(
            self,
            instance: Fixture[WhitelistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'fetch_source_contents',
            lambda foo, bar: None
        )

        instance.fetch_source_contents(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'Fetching whitelisted domains from' \
                         f' {self.sample_source_url}\n'
