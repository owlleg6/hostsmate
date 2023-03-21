import logging

from khostman.utils.os_utils import OSUtils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t[%(levelname)s]\t%(message)s')

project_root = OSUtils.get_project_root()
logs_dir = project_root / 'logs'

if not logs_dir.exists():
    logs_dir.mkdir()

file_handler = logging.FileHandler(f'{project_root}/logs/hosts.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
