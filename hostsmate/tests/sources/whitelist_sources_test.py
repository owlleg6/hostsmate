import pytest
from typing import Union

from hostsmate.sources.sources import Sources
from hostsmate.sources.whitelist_sources import WhitelistSources

Fixture = Union


class TestWhitelistSources:
    sample_source_url = 'https://foobarzar.com/hosts.txt'

    @staticmethod
    @pytest.fixture
    def instance():
        return WhitelistSources()

    @staticmethod
    def test_sources_json_path(instance: Fixture):
        assert instance.sources_json_path.exists()
        assert instance.sources_json_path.parent.name == 'resources'
        assert instance.sources_json_path.name == 'whitelist_sources.json'

    def test_add_url_to_sources(
            self,
            instance: Fixture,
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture
    ):
        monkeypatch.setattr(
            Sources, 'add_url_to_sources',
            lambda foo, bar: None
        )

        instance.add_url_to_sources(self.sample_source_url)
        assert capsys.readouterr().out == \
               f'"{self.sample_source_url}" has been added to whitelist sources.\n'

    def test_remove_url_from_sources(
            self,
            instance: Fixture,
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture
    ):
        monkeypatch.setattr(
            Sources, 'remove_url_from_sources',
            lambda foo, bar: None
        )

        instance.remove_url_from_sources(self.sample_source_url)
        assert capsys.readouterr().out == \
               f'"{self.sample_source_url}" has been removed from whitelist sources.\n'

    def test_fetch_source_contents(
            self,
            instance: Fixture,
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture
    ):
        monkeypatch.setattr(
            Sources, 'fetch_source_contents',
            lambda foo, bar: None
        )

        instance.fetch_source_contents(self.sample_source_url)
        assert capsys.readouterr().out == \
               f'Fetching whitelisted domains from {self.sample_source_url}\n'
