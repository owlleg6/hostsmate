import pytest
from typing import Union

from hostsmate_src.sources.blacklist_sources import BlacklistSources
from hostsmate_src.sources.sources import Sources

Fixture = Union


class TestBlacklistSources:

    sample_source_url: str = 'https://foobarzar.com/hosts.txt'

    @staticmethod
    @pytest.fixture
    def instance():
        return BlacklistSources()

    @staticmethod
    def test_sources_json_path(instance: Fixture):  # type: ignore
        assert instance.sources_json_path.exists()  # type: ignore
        assert instance.sources_json_path.parent.name == 'resources'  # type: ignore
        assert instance.sources_json_path.name == 'blacklist_sources.json'  # type: ignore

    def test_add_url_to_sources(
            self,
            instance: Fixture[BlacklistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'add_url_to_sources',
            lambda foo, bar: None
        )

        instance.add_url_to_sources(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'"{self.sample_source_url}"' \
                         f' has been added to blacklist sources.\n'

    def test_remove_url_from_sources(
            self,
            instance: Fixture[BlacklistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'remove_url_from_sources',
            lambda foo, bar: None
        )

        instance.remove_url_from_sources(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'"{self.sample_source_url}"' \
                         f' has been removed from blacklist sources.\n'

    def test_fetch_source_contents(
            self,
            instance: Fixture[BlacklistSources],  # type: ignore
            monkeypatch: pytest.MonkeyPatch,
            capsys: Fixture  # type: ignore
    ):
        monkeypatch.setattr(
            Sources, 'fetch_source_contents',
            lambda foo, bar: None
        )
        instance.fetch_source_contents(self.sample_source_url)  # type: ignore
        stdout = capsys.readouterr().out  # type: ignore
        assert stdout == f'Fetching blacklisted domains from ' \
                         f'{self.sample_source_url}\n'
