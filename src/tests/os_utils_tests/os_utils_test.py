import subprocess
from typing import Union
from pathlib import Path

import pytest

from utils.os_utils import OSUtils

Fixture = Union


def raise_subprocess_err(_, stdout=None):
    raise subprocess.SubprocessError


def test_get_project_root_returns_path_obj():
    root_path: Path = OSUtils().get_project_root()
    assert isinstance(root_path, Path)


def test_get_project_root_is_dir():
    root_path: Path = OSUtils().get_project_root()
    assert root_path.is_dir()


def test_get_project_root_ensure_correct_dir():
    root_path: Path = OSUtils().get_project_root()
    assert (root_path / 'resources').is_dir()


@pytest.mark.parametrize('platform, exp_res', [
    ('linux', True),
    ('freebsd', True),
    ('darwin', False),
    ('win32', False)
])
def test_ensure_linux_or_bsd(platform: str, exp_res: bool):
    result: bool = OSUtils.ensure_linux_or_bsd(platform)
    assert result == exp_res


def test_execute_sh_command_as_root(tmp_path: Fixture[Path]):  # type: ignore
    program_to_run: Path = tmp_path / 'prog.sh'  # type: ignore
    program_to_run.touch()
    program_to_run.chmod(1)
    assert OSUtils().execute_sh_command_as_root(program_to_run, [])


def test_execute_sh_command_as_root_raises_sys_exit(
        monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        subprocess, 'run', raise_subprocess_err
    )
    with pytest.raises(SystemExit):
        OSUtils().execute_sh_command_as_root('grep', [])


def test_is_shell_dependency_installed():
    assert OSUtils().is_shell_dependency_installed('grep')


def test_is_shell_dependency_installed_raises_sys_exit(
        monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        subprocess, 'run', raise_subprocess_err
    )
    with pytest.raises(SystemExit):
        OSUtils().is_shell_dependency_installed('grep')