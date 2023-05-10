from unittest.mock import patch
from pathlib import Path
import uuid

import pytest

from hostsmate_src.domains_extractor import DomainsExtractor
from hostsmate_src.unique_blacklisted_domains import UniqueBlacklistedDomains


@pytest.fixture
def temp_raw_file(tmp_path):
    temp_file: Path = tmp_path / 'test.txt'
    with temp_file.open('w') as f:
        f.write('0.0.0.0 example1.com # comment\n'
                '127.0.0.1 example2.com\n'
                'whitelisted.net\n'
                'whitelisted.org\n'
                'example3.com # comment\n'
                '# comment\n'
                '\n'
                '::1 example4.com\n'
                '<a href="example4.com">hosts<a>')
    return temp_file


@pytest.fixture
def dom_extr_instance(temp_raw_file):
    return DomainsExtractor(temp_raw_file)


@pytest.mark.parametrize(
    'raw_line, domain', [
        ('0.0.0.0 example.com', '0.0.0.0 example.com\n'),
        ('0.0.0.0 example.com #hello', '0.0.0.0 example.com\n'),
        ('0.0.0.0 example.com hello world', '0.0.0.0 example.com\n')
    ])
def test__extract_domain_if_starts_with_non_rout_ip(
        dom_extr_instance,
        raw_line,
        domain
):
    assert dom_extr_instance._extract_domain_if_starts_with_non_rout_ip(
        raw_line
    ) == domain


@pytest.mark.parametrize(
    'raw_line, domain', [
        ('127.0.0.1', ''),
        ('127.0.0.1 example.com', 'example.com\n'),
        ('127.0.0.1 example.com #hello', 'example.com\n'),
        ('127.0.0.1 example.com hello world', 'example.com\n')
    ])
def test__extract_domain_if_starts_with_localhost_ip(
        dom_extr_instance,
        raw_line,
        domain
):
    assert dom_extr_instance._extract_domain_if_starts_with_localhost_ip(
        raw_line
    ) == domain


@pytest.mark.parametrize(
    'raw_line, domain', [
        ('No domain here', ''),
        ('Today is a sunny day. Here is the domain: example.com', 'example.com\n'),
        ('example.com', 'example.com\n'),
        ('example.com # hello world', 'example.com\n'),
        ('example.com.au', 'example.com.au\n'),
        ('io.com.au.gov', 'io.com.au.gov\n'),
    ])
def test__extract_domain_with_regex(
        dom_extr_instance,
        raw_line,
        domain
):
    assert dom_extr_instance._extract_domain_with_regex(
        raw_line
    ) == domain


@pytest.mark.parametrize(
    'raw_line, domain', [
        ('0.0.0.0 example.com #hello', '0.0.0.0 example.com\n'),
        ('127.0.0.1 example.com #hello', 'example.com\n'),
        ('io.com.au.gov', 'io.com.au.gov\n'),
    ])
def test_extract_domain_from_line(
        dom_extr_instance,
        raw_line,
        domain
):
    assert dom_extr_instance.extract_domain_from_line(
        raw_line
    ) == domain


def test_extract_domain_to_unique_domains_set(dom_extr_instance):
    with patch(
            'hostsmate_src.sources.whitelist_sources.WhitelistSources.'
            'get_lines_of_all_sources_contents'
    ) as mock_whitelist:
        mock_whitelist.return_value = {'whitelisted.net\n', 'whitelisted.org\n'}
        dom_extr_instance.extract_domain_to_unique_domains_set()

    assert UniqueBlacklistedDomains().items == {
        '0.0.0.0 example1.com\n',
        '0.0.0.0 example2.com\n',
        '0.0.0.0 example3.com\n'
    }


def test_extract_domain_to_unique_domains_set_raises_sys_exit():
    while True:
        non_existing_path = Path().home() / uuid.uuid4().hex
        if non_existing_path.exists():
            continue
        else:
            break
    with pytest.raises(SystemExit):
        DomainsExtractor(non_existing_path).extract_domain_to_unique_domains_set()
