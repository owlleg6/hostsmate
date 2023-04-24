import sys
from datetime import date, datetime

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from freezegun import freeze_time

import hostsmate.unique_blacklisted_domains
from utils.str_utils import StringUtils
from hostsmate.system_hosts_file import SystemHostsFile
from hostsmate.unique_blacklisted_domains import UniqueBlacklistedDomains

test_domains_to_add = [
    'malware-domain.com',
    'one-more-malware-domain.com',
    'unwanted-ads.com',
]

test_domains_to_remove = [
    'example.com',
    'another-example.com',
    'blacklisted-domain.com',
]


@pytest.fixture
def sys_hosts_file(tmp_path):
    hosts_sample_path = tmp_path / 'hosts'
    with open(hosts_sample_path, 'w') as hosts:
        hosts.write("# Start of the user's custom domains\n"
                    '\n'
                    '0.0.0.0 example.com\n'
                    '0.0.0.0 another-example.com\n'
                    '0.0.0.0 blacklisted-domain.com\n'
                    '\n'
                    "# End of the user's custom domains\n"
                    '\n'
                    '0.0.0.0 domain-smaple.com\n'
                    '0.0.0.0 domain-to-whitelist.com\n')
        return Path(hosts_sample_path)


@pytest.fixture
def remove_or_add_domain_setup(
        monkeypatch,
        sys_hosts_file,
        domain
):
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)

    with patch(
            'utils.str_utils.StringUtils.strip_domain_prefix'
    ) as mock_strip_domain_prefix:
        mock_strip_domain_prefix.return_value = domain


def test_header_path_is_a_file():
    header_path: Path = SystemHostsFile()._header_path
    assert header_path.is_file()


def test_header_path_in_expected_dir():
    header_path: Path = SystemHostsFile()._header_path
    assert header_path.parent.name == 'resources'


@pytest.mark.parametrize('platform, exp_path', [
    ('linux', Path('/etc/hosts')),
    ('freebsd', Path('/etc/hosts')),
    ('darwin', Path('/etc/hosts')),
    ('cygwin', Path('/etc/hosts'))
])
def test_original_path(
        monkeypatch,
        platform,
        exp_path
):
    monkeypatch.setattr(sys, 'platform', platform)
    assert SystemHostsFile().original_path == exp_path


def test_renamed_path(monkeypatch, tmp_path):
    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        tmp_path / 'hosts_mock'
    )
    assert SystemHostsFile().renamed_path == tmp_path / 'hosts_mock.tmp'


def test__get_user_custom_domains_if_hosts_does_not_exist(monkeypatch):

    monkeypatch.setattr(
        SystemHostsFile, 'original_path',
        Path('/fake/path/')
    )
    assert SystemHostsFile()._get_user_custom_domains() == set()


def test__get_user_custom_domains_returns_domains_from_present_hosts_file(
        monkeypatch,
        sys_hosts_file
):
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)
    assert SystemHostsFile()._get_user_custom_domains() == {
        '0.0.0.0 example.com',
        '0.0.0.0 another-example.com',
        '0.0.0.0 blacklisted-domain.com'
    }


@pytest.mark.parametrize('domain', test_domains_to_add)
def test_add_blacklisted_domain(
        monkeypatch,
        sys_hosts_file,
        domain,
        remove_or_add_domain_setup
):
    SystemHostsFile().add_blacklisted_domain(
        f'https://{domain}'
    )
    assert f'0.0.0.0 {domain}\n' in open(sys_hosts_file).readlines()


def test_add_blacklisted_domain_os_error(
        sys_hosts_file,
        capsys
):
    with patch('builtins.open', MagicMock(side_effect=OSError)):
        SystemHostsFile().add_blacklisted_domain('failed-adding.com')
    assert f'0.0.0.0 failed-adding.com\n' not in open(sys_hosts_file).readlines()
    assert capsys.readouterr().out == 'Operation failed.\n'


@pytest.mark.parametrize('domain', test_domains_to_remove)
def test_remove_domain(
        monkeypatch,
        sys_hosts_file,
        domain,
        remove_or_add_domain_setup
):
    SystemHostsFile().remove_domain(domain)
    assert f'0.0.0.0 {domain}\n' not in open(sys_hosts_file).readlines()


def test_remove_domain_os_error(
        sys_hosts_file,
        capsys
):
    with patch('builtins.open', MagicMock(side_effect=OSError)):
        SystemHostsFile().remove_domain('example.com')
    assert f'0.0.0.0 example.com\n' in open(sys_hosts_file).readlines()
    assert capsys.readouterr().out == 'Operation failed.\n'


def test_create_backup(
        tmp_path,
        monkeypatch,
        sys_hosts_file,
):
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)
    backup_file = SystemHostsFile().create_backup(tmp_path)
    assert open(sys_hosts_file).read() == open(backup_file).read()


def test_create_backup_os_error(capsys):
    SystemHostsFile().create_backup('/non/existing/path')
    assert capsys.readouterr().out == 'Error creating backup.\n'


@pytest.fixture
@freeze_time('2020-04-20')
def test__get_header(monkeypatch):
    custom_domains = {f'0.0.0.0 {domain}' for domain in test_domains_to_add}
    amount_of_blacklisted_domains = '1,232,245'

    monkeypatch.setattr(
        SystemHostsFile, '_get_user_custom_domains',
        lambda _: custom_domains
    )
    monkeypatch.setattr(
        StringUtils, 'sep_num_with_commas',
        lambda _: amount_of_blacklisted_domains
    )

    result = SystemHostsFile()._get_header()

    assert amount_of_blacklisted_domains in result
    assert all(domain in result for domain in custom_domains)
    assert '2020-04-20' in result

    return result


def test_build(tmp_path, monkeypatch):
    mock_formatted_num_of_domains = '1,232,245'
    mock_header = '\n\nheader_mock\n\n'
    mock_hosts_file = tmp_path / 'built_hosts_file'
    mock_blacklisted_domains = {f'0.0.0.0 {domain}\n' for domain in test_domains_to_remove}

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

    SystemHostsFile().build()

    with open(mock_hosts_file) as built_hosts:
        result = built_hosts.read()

        assert all(domain in result for domain in mock_blacklisted_domains)
        assert mock_header in result
