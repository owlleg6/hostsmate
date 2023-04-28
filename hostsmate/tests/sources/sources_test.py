import json
from typing import Union
from pathlib import Path

import pytest
import responses

from hostsmate.sources.sources import Sources

Fixture = Union


class TestSources(Sources):

    present_sources: list[str] = [
        'https://example.com/hosts.txt',
        'https://another-example.com/hosts',
        'https://one-more-example.com/hosts_file',
        'https://example-1.com/hosts_file.txt',
        'https://example-2.com/hosts_file.txt',
        'https://example-3.com/hosts_file.txt'
    ]

    test_urls_to_add: set[str] = {
        'https://test1.com.au',
        'https://test-2.co.uk',
        'https://test4.gov.us',
    }

    test_links_to_remove: set[str] = {
        'https://example-1.com/hosts_file.txt',
        'https://example-2.com/hosts_file.txt',
        'https://example-3.com/hosts_file.txt'
    }

    test_link_for_get_request: str = 'https://foobarzar.com'

    mock_resp_contents: str = \
        '\n'.join(f'blacklisted-domain-{i}.su' for i in range(1, 31))

    @pytest.fixture
    def sources_file_setup_method(self, tmp_path: Fixture[Path]):
        self.tmp_sources_path: Path = tmp_path / 'sources.json'
        contents = {
            'sources': self.present_sources
        }
        with open(self.tmp_sources_path, 'w') as sources:
            json.dump(contents, sources)

    @staticmethod
    @pytest.fixture
    def file_to_append_contents(tmp_path: Fixture[Path]) -> Path:
        path: Path = tmp_path / 'contents_dump'
        path.touch()
        return path

    @property
    def sources_json_path(self) -> Path:
        return self.tmp_sources_path

    def test_source_urls(
            self,
            sources_file_setup_method: Fixture
    ):
        assert all(
            source_url in self.sources_urls for source_url in self.present_sources
        )

    @pytest.mark.parametrize('test_link', test_urls_to_add)
    def test_add_url_to_sources(
            self,
            tmp_path: Fixture[Path],
            sources_file_setup_method: Fixture,
            test_link: str
    ):
        super().add_url_to_sources(test_link)
        assert test_link in self.sources_urls

    @pytest.mark.parametrize(
        'test_link',
        test_links_to_remove
    )
    def test_remove_url_from_sources(
            self,
            sources_file_setup_method: Fixture[Path],
            test_link: str
    ):
        super().remove_url_from_sources(test_link)
        assert test_link not in self.sources_urls

    @responses.activate
    def test_fetch_source_contents(self):
        responses.add(
            responses.GET,
            self.test_link_for_get_request,
            self.mock_resp_contents,
            status=200
        )
        assert self.fetch_source_contents(self.test_link_for_get_request) == \
               self.mock_resp_contents

    @responses.activate
    def test_fetch_source_http_error(self):
        responses.add(
            responses.GET,
            self.test_link_for_get_request,
            self.mock_resp_contents,
            status=403
        )
        assert self.fetch_source_contents(self.test_link_for_get_request) == ''

    @responses.activate
    def test_append_source_contents_to_file(
            self,
            file_to_append_contents: Fixture[Path],
            monkeypatch: pytest.MonkeyPatch
    ):
        responses.add(
            responses.GET,
            self.test_link_for_get_request,
            self.mock_resp_contents,
            status=200
        )
        self.append_source_contents_to_file(
            self.test_link_for_get_request, file_to_append_contents
        )
        assert self.mock_resp_contents in file_to_append_contents.read_text()

    def test_append_sources_contents_to_file_concurrently(
            self,
            file_to_append_contents: Fixture[Path],
            monkeypatch: pytest.MonkeyPatch,
    ):
        monkeypatch.setattr(
            TestSources,
            'sources_urls',
            self.test_urls_to_add
        )
        monkeypatch.setattr(
            self,
            'append_source_contents_to_file',
            lambda _: None
        )
        result: int = self.append_sources_contents_to_file_concurrently(
            file_to_append_contents
        )
        assert result == len(self.test_urls_to_add)
