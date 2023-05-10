import pytest
from hostsmate_src.suspender import Suspender


@pytest.fixture
def suspender(tmp_path):
    """
    A pytest fixture that creates a temporary file for the Hosts file and returns a `Suspender` instance
    configured to use it.
    """
    hosts_file = tmp_path / 'hosts'
    with open(hosts_file, 'w') as f:
        f.write('foo bar')

    original_hosts_path = Suspender.org_hosts_name
    Suspender.org_hosts_name = hosts_file

    yield Suspender()

    Suspender.org_hosts_name = original_hosts_path


def test_suspend(suspender):
    suspender.suspend()
    assert not Suspender.org_hosts_name.exists()
    assert Suspender.renamed_hosts.exists()


def test_suspend_raises_sys_exit(tmp_path):
    """
    Test that `suspend()` raises a `SystemExit` exception when the Hosts file is not found.
    """
    s = Suspender()
    s.org_hosts_name = tmp_path / 'non_existent_file'
    with pytest.raises(SystemExit):
        s.suspend()


def test_resume(suspender):
    suspender.suspend()
    suspender.resume()
    assert not Suspender.renamed_hosts.exists()
    assert Suspender.org_hosts_name.exists()


def test_resume_raises_sys_exit(tmp_path):
    """
    Test that `resume()` raises a `SystemExit` exception when the renamed Hosts file is not found.
    """
    s = Suspender()
    s.renamed_hosts = tmp_path / 'non_existent_file'
    with pytest.raises(SystemExit):
        s.resume()
