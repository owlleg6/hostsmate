from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from hostsmate.system_hosts_file import SystemHostsFile

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
def sys_hosts_file_instance(tmp_path):
    return SystemHostsFile()


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
        sys_hosts_file_instance,
        domain
):
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)

    with patch(
            'utils.str_utils.StringUtils.strip_domain_prefix'
    ) as mock_strip_domain_prefix:
        mock_strip_domain_prefix.return_value = domain


def test_header_path_is_a_file(sys_hosts_file_instance):
    header_path = sys_hosts_file_instance._header_path
    assert header_path.is_file()


def test_header_path_in_expected_dir(sys_hosts_file_instance):
    header_path = sys_hosts_file_instance._header_path
    assert header_path.parent.name == 'resources'


@pytest.mark.parametrize('platform, exp_path', [
    ('linux', Path('/etc/hosts')),
    ('freebsd', Path('/etc/hosts')),
    ('darwin', Path('/etc/hosts')),
    ('cygwin', Path('/etc/hosts'))
])
def test_original_path(
        sys_hosts_file_instance,
        platform,
        exp_path
):
    with patch('sys.platform') as mock_platform:
        mock_platform.return_value = platform
        assert sys_hosts_file_instance.original_path == exp_path


def test_renamed_path(sys_hosts_file_instance):
    assert sys_hosts_file_instance.renamed_path == Path('/etc/hosts.tmp')


@patch(
    'hostsmate.system_hosts_file.SystemHostsFile.original_path',
    new=Path('/fake/path/')
)
def test__get_user_custom_domains_if_hosts_does_not_exist():
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
        sys_hosts_file_instance,
        domain,
        remove_or_add_domain_setup
):
    sys_hosts_file_instance.add_blacklisted_domain(
        f'https://{domain}'
    )
    assert f'0.0.0.0 {domain}\n' in open(sys_hosts_file).readlines()


def test_add_blacklisted_domain_os_error(
        sys_hosts_file_instance,
        sys_hosts_file,
        capsys
):
    with patch('builtins.open', MagicMock(side_effect=OSError)):
        sys_hosts_file_instance.add_blacklisted_domain('failed-adding.com')
    assert f'0.0.0.0 failed-adding.com\n' not in open(sys_hosts_file).readlines()
    assert capsys.readouterr().out == 'Operation failed.\n'


@pytest.mark.parametrize('domain', test_domains_to_remove)
def test_remove_domain(
        monkeypatch,
        sys_hosts_file,
        sys_hosts_file_instance,
        domain,
        remove_or_add_domain_setup
):
    sys_hosts_file_instance.remove_domain(domain)
    assert f'0.0.0.0 {domain}\n' not in open(sys_hosts_file).readlines()


def test_remove_domain_os_error(
        sys_hosts_file_instance,
        sys_hosts_file,
        capsys
):
    with patch('builtins.open', MagicMock(side_effect=OSError)):
        sys_hosts_file_instance.remove_domain('example.com')
    assert f'0.0.0.0 example.com\n' in open(sys_hosts_file).readlines()
    assert capsys.readouterr().out == 'Operation failed.\n'


def test_create_backup(
        tmp_path,
        monkeypatch,
        sys_hosts_file,
        sys_hosts_file_instance,
):
    monkeypatch.setattr(SystemHostsFile, 'original_path', sys_hosts_file)
    backup_file = sys_hosts_file_instance.create_backup(tmp_path)
    assert open(sys_hosts_file).read() == open(backup_file).read()


def test_create_backup_os_error(capsys):
    SystemHostsFile().create_backup('/non/existing/path')
    assert capsys.readouterr().out == 'Error creating backup.\n'