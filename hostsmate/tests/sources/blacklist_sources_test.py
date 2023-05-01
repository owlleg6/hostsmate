import pytest
from typing import Union

from hostsmate.sources.blacklist_sources import BlacklistSources
from hostsmate.sources.sources import Sources

Fixture = Union


class TestBlacklistSources:
    sample_source_url = 'https://foobarzar.com/hosts.txt'

    @staticmethod
    @pytest.fixture
    def instance():
        return BlacklistSources()

    @staticmethod
    def test_sources_json_path(instance: Fixture):
        assert instance.sources_json_path.exists()
        assert instance.sources_json_path.parent.name == 'resources'
        assert instance.sources_json_path.name == 'blacklist_sources.json'

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
               f'"{self.sample_source_url}" has been added to blacklist sources.\n'

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
               f'"{self.sample_source_url}" has been removed from blacklist sources.\n'

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
               f'Fetching blacklisted domains from {self.sample_source_url}\n'
