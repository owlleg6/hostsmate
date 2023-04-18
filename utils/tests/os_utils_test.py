from pathlib import Path

from utils.os_utils import OSUtils


def test_get_project_root_returns_path_obj():
    root_path: Path = OSUtils().get_project_root()
    assert isinstance(root_path, Path)


def test_get_project_root_is_dir():
    root_path: Path = OSUtils().get_project_root()
    assert root_path.is_dir()


def test_get_project_root_ensure_correct_dir():
    root_path: Path = OSUtils().get_project_root()
    assert (root_path / 'hostsmate.py').is_file()
