import sys
from pathlib import Path
from typing import Union

import pytest
from freezegun import freeze_time

from utils.str_utils import StringUtils
from hostsmate_src.system_hosts_file import SystemHostsFile
from hostsmate_src.unique_blacklisted_domains import UniqueBlacklistedDomains

Fixture = Union
unix_like_hosts_path: Path = Path('/etc/hosts')
mock_current_time: str = '2020-04-20'
mock_formatted_num_of_domains: str = '1,232,245'

domains_to_add: list[str] = [
    'malware-domain.com',
    'one-more-malware-domain.com',
    'unwanted-ads.com',
]
domains_to_remove: list[str] = [
    'example.com',
    'another-example.com',
    'blacklisted-domain.com',
]


@pytest.fixture
def sys_hosts_file(tmp_path: Fixture[Path]) -> Path:  # type: ignore
    """Sample of the already built Hosts file.

    Returns:
        Path: path to the sample temporary Hosts file.
    """
    hosts_sample_path: Path = tmp_path / 'hosts'  # type: ignore
    with open(hosts_sample_path, 'w') as hosts:
        hosts.write("# Start of the user's custom domains\n"
                    '\n'
                    '0.0.0.0 example.com\n'
                    '0.0.0.0 another-example.com\n'
                    '0.0.0.0 blacklisted-domain.com\n'
                    '\n'
                    "# End of the user's custom domains\n"
                    '\n'
                    '0.0.0.0 domain-sample.com\n'
                    '0.0.0.0 domain-to-whitelist.com\n')
        return Path(hosts_sample_path)


@pytest.fixture
def non_existing_hosts_path() -> Path:
    return Path('/non/existing/path')


@pytest.fixture
def remove_or_add_domain_setup(
        monkeypatch: pytest.MonkeyPatch,
        sys_hosts_file: Path,
        domain: str
):
    """
    Mock SystemHostsFile.original_path and StringUtils.strip_domain_prefix
    return values.
    """
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)
    monkeypatch.setattr(StringUtils, 'strip_domain_prefix', lambda _: domain)


def test_header_path_is_a_file():
    """Path to a header is a file."""
    header_path: Path = SystemHostsFile()._header_path
    assert header_path.is_file()


def test_header_path_in_expected_dir():
    """Path to a header is in the resources directory."""
    header_path: Path = SystemHostsFile()._header_path
    assert header_path.parent.name == 'resources'


@pytest.mark.parametrize('platform, exp_path', [
    ('linux', unix_like_hosts_path),
    ('freebsd', unix_like_hosts_path),
    ('darwin', unix_like_hosts_path),
    ('cygwin', unix_like_hosts_path)
])
def test_original_path(
        monkeypatch: pytest.MonkeyPatch,
        platform: str,
        exp_path: Path
):
    """Correctness of the returned path to the system Hosts file."""
    monkeypatch.setattr(
        sys, 'platform',
        platform
    )
    assert SystemHostsFile().original_path == exp_path


def test_original_path_raises_sys_exit(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, 'platform',
        'win32'
    )
    with pytest.raises(SystemExit):
        SystemHostsFile().original_path


def test_renamed_path(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Fixture[Path]  # type: ignore
):
    """Correctness of the renamed_path to the system Hosts file."""
    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        tmp_path / 'hosts_mock'  # type: ignore
    )
    assert SystemHostsFile().renamed_path == tmp_path / 'hosts_mock.tmp'  # type: ignore


def test__get_user_custom_domains_if_hosts_does_not_exist(
        monkeypatch: pytest.MonkeyPatch,
        non_existing_hosts_path: Fixture[Path]  # type: ignore
):
    """Return empty set if the Hosts file does not exist."""
    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        non_existing_hosts_path
    )
    assert SystemHostsFile()._get_user_custom_domains() == set()


def test__get_user_custom_domains_returns_domains_from_present_hosts_file(
        monkeypatch: pytest.MonkeyPatch,
        sys_hosts_file: Fixture[Path]  # type: ignore
):
    """
    Return all the listed domains from the custom domains section of the Hosts file.
    """
    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        sys_hosts_file
    )
    assert SystemHostsFile()._get_user_custom_domains() == {
        '0.0.0.0 example.com',
        '0.0.0.0 another-example.com',
        '0.0.0.0 blacklisted-domain.com'
    }


@pytest.mark.parametrize('domain', domains_to_add)
def test_add_blacklisted_domain(
        monkeypatch: pytest.MonkeyPatch,
        sys_hosts_file: Fixture[Path],  # type: ignore
        domain: str,
        remove_or_add_domain_setup: Fixture[None]  # type: ignore
):
    """Write domain to the Hosts file with 0.0.0.0 prefix."""
    SystemHostsFile().add_blacklisted_domain(
        f'https://{domain}'
    )
    assert f'0.0.0.0 {domain}\n' in open(sys_hosts_file).readlines()


@pytest.mark.parametrize('domain', domains_to_remove)
def test_remove_domain(
        monkeypatch: pytest.MonkeyPatch,
        sys_hosts_file: Fixture[Path],  # type: ignore
        domain: str,
        remove_or_add_domain_setup: Fixture[None]  # type: ignore
):
    """Remove domain name from the Hosts file."""
    SystemHostsFile().remove_domain(domain)
    assert f'0.0.0.0 {domain}\n' not in open(sys_hosts_file).readlines()


def test_create_backup(
        tmp_path: Fixture[Path],  # type: ignore
        monkeypatch: pytest.MonkeyPatch,
        sys_hosts_file: Fixture[Path],  # type: ignore
):
    """Backup file has the same contents as the original Hosts."""
    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        sys_hosts_file
    )
    backup_file: Path = SystemHostsFile().create_backup(tmp_path)
    assert open(sys_hosts_file).read() == open(backup_file).read()


@freeze_time(mock_current_time)
def test__get_header(monkeypatch: pytest.MonkeyPatch):
    """
    Header is formatted with the correct date, amount of blacklisted domains
    and all the custom domains from the present Hosts file are listed.
    """
    custom_domains: set = {f'0.0.0.0 {domain}' for domain in domains_to_add}

    monkeypatch.setattr(
        SystemHostsFile, '_get_user_custom_domains',
        lambda _: custom_domains
    )
    monkeypatch.setattr(
        StringUtils, 'sep_num_with_commas',
        lambda _: mock_formatted_num_of_domains
    )

    result: str = SystemHostsFile()._get_header()

    assert mock_formatted_num_of_domains in result
    assert all(domain in result for domain in custom_domains)
    assert mock_current_time in result


def test_build(
        tmp_path: Fixture[Path],  # type: ignore
        monkeypatch: pytest.MonkeyPatch
):
    """Header and all the blacklisted domains are present in the newly
    created Hosts file"""
    mock_header: str = '\n\nheader_mock\n\n'
    mock_hosts_file: Path = tmp_path / 'built_hosts_file'  # type: ignore
    mock_blacklisted_domains: set = \
        {f'0.0.0.0 {domain}\n' for domain in domains_to_remove}

    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        mock_hosts_file
    )
    monkeypatch.setattr(
        UniqueBlacklistedDomains, 'items',
        mock_blacklisted_domains
    )
    monkeypatch.setattr(
        StringUtils, 'sep_num_with_commas',
        lambda _: mock_formatted_num_of_domains)
    monkeypatch.setattr(
        SystemHostsFile, '_get_header',
        lambda _: mock_header)

    SystemHostsFile()._build()

    with open(mock_hosts_file) as built_hosts:
        result: str = built_hosts.read()

        assert all(domain in result for domain in mock_blacklisted_domains)
        assert mock_header in result
