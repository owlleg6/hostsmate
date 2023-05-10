import json
from typing import Union
from pathlib import Path

import pytest
import responses

from hostsmate_src.sources.sources import Sources

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

    test_urls_to_remove: set[str] = {
        'https://example-1.com/hosts_file.txt',
        'https://example-2.com/hosts_file.txt',
        'https://example-3.com/hosts_file.txt'
    }

    test_url_for_get_request: str = 'https://foobarzar.com'

    mock_resp_contents: str = \
        '\n'.join(f'blacklisted-domain-{i}.su' for i in range(1, 31))

    @pytest.fixture
    def sources_file_setup_method(self, tmp_path: Fixture[Path]) -> None:  # type: ignore
        self.tmp_sources_path: Path = tmp_path / 'sources.json'  # type: ignore
        contents = {
            'sources': self.present_sources
        }
        with open(self.tmp_sources_path, 'w') as sources:
            json.dump(contents, sources)

    @staticmethod
    @pytest.fixture
    def file_to_append_contents(tmp_path: Fixture[Path]) -> Path:  # type: ignore
        path: Path = tmp_path / 'contents_dump'  # type: ignore
        path.touch()
        return path

    @property
    def sources_json_path(self) -> Path:
        return self.tmp_sources_path

    def test_source_urls(
            self,
            sources_file_setup_method: Fixture  # type: ignore
    ):
        assert all(
            source_url in self.sources_urls for source_url in self.present_sources
        )

    @pytest.mark.parametrize('test_link', test_urls_to_add)
    def test_add_url_to_sources(
            self,
            tmp_path: Fixture[Path],  # type: ignore
            sources_file_setup_method: Fixture,  # type: ignore
            test_link: str
    ):
        self.add_url_to_sources(test_link)
        assert test_link in self.sources_urls

    def test_add_url_to_sources_if_source_already_present(
            self,
            sources_file_setup_method: Fixture  # type: ignore
    ):
        with pytest.raises(SystemExit):
            self.add_url_to_sources(self.present_sources[0])

    @pytest.mark.parametrize(
        'test_url',
        test_urls_to_remove
    )
    def test_remove_url_from_sources(
            self,
            sources_file_setup_method: Fixture,  # type: ignore
            test_url: str
    ):
        self.remove_url_from_sources(test_url)
        assert test_url not in self.sources_urls

    def test_remove_url_from_sources_if_source_is_not_present(
            self,
            sources_file_setup_method: Fixture  # type: ignore
    ):
        with pytest.raises(SystemExit):
            self.remove_url_from_sources('https://url.not.in.sources')

    @responses.activate
    def test_fetch_source_contents(self):
        responses.add(
            responses.GET,
            self.test_url_for_get_request,
            self.mock_resp_contents,
            status=200
        )
        assert self.fetch_source_contents(self.test_url_for_get_request) == \
               self.mock_resp_contents

    @responses.activate
    def test_fetch_source_http_error(self):
        responses.add(
            responses.GET,
            self.test_url_for_get_request,
            self.mock_resp_contents,
            status=403
        )
        assert self.fetch_source_contents(self.test_url_for_get_request) == ''

    @responses.activate
    def test_append_source_contents_to_file(
            self,
            file_to_append_contents: Fixture[Path]  # type: ignore
    ):
        responses.add(
            responses.GET,
            self.test_url_for_get_request,
            self.mock_resp_contents,
            status=200
        )
        self.append_source_contents_to_file(
            self.test_url_for_get_request, file_to_append_contents
        )
        assert self.mock_resp_contents in file_to_append_contents.read_text()  # type: ignore

    def test_append_sources_contents_to_file_concurrently(
            self,
            file_to_append_contents: Fixture[Path],  # type: ignore
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

    @responses.activate
    def test_get_lines_of_all_sources_contents(
            self,
            sources_file_setup_method: Fixture  # type: ignore
    ):
        mock_resp: str = 'FooBar\nBarZoo\nDar\nTanDan\n'
        exp_result: set = {'FooBar\n', 'BarZoo\n', 'Dar\n', 'TanDan\n'}

        for source_url in self.present_sources:
            responses.add(
                responses.GET,
                source_url,
                mock_resp,
                status=200
            )
        result: set = self.get_lines_of_all_sources_contents()
        assert result == exp_result
