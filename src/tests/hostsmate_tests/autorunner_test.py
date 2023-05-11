import pytest
from typing import Union

from hostsmate_src.autorunner import Autorunner
from hostsmate_src.cli.prompt import Prompt
from utils.os_utils import OSUtils

Fixture = Union


def test_correct_hostsmate_app_path():
    assert Autorunner.hostsmate_executable.name == 'execute.py'


def test_correct_shell_script_path():
    assert Autorunner.job_setter_sh_script_path.name == \
                                                'anacron_job_setter.sh'


def test_run_anacron_setter_sh_script(
        monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        OSUtils, 'execute_sh_command_as_root',
        lambda foo, bar, zar: True
    )
    assert Autorunner().run_anacron_setter_sh_script('foo_bar.sh')


def test_run_anacron_setter_sh_script_failed(
        monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        OSUtils, 'execute_sh_command_as_root',
        lambda foo, bar, zar: False
    )
    assert not Autorunner().run_anacron_setter_sh_script('foo_bar.sh')


def test_set_up_anacron_job(
        monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(
        OSUtils, 'ensure_linux_or_bsd',
        lambda _: True
    )
    monkeypatch.setattr(
        OSUtils, 'is_shell_dependency_installed',
        lambda foo, bar: True
    )
    monkeypatch.setattr(
        Prompt, 'ask_autorun_frequency',
        lambda _: 'foo'
    )
    monkeypatch.setattr(
        Autorunner, 'run_anacron_setter_sh_script',
        lambda foo, bar: True
    )
    assert Autorunner().set_up_anacron_job()


def test_set_up_anacron_job_raises_sys_exit(
        monkeypatch: pytest.MonkeyPatch,
        capsys: Fixture
):
    monkeypatch.setattr(
        OSUtils, 'ensure_linux_or_bsd',
        lambda _: True
    )
    monkeypatch.setattr(
        OSUtils, 'is_shell_dependency_installed',
        lambda foo, bar: False
    )
    monkeypatch.setattr(
        Prompt, 'ask_autorun_frequency',
        lambda _: 'foo'
    )
    monkeypatch.setattr(
        Autorunner, 'run_anacron_setter_sh_script',
        lambda foo, bar: True
    )
    with pytest.raises(SystemExit):
        Autorunner().set_up_anacron_job()
