import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s\t[%(levelname)s]\t%(message)s')
project_root = Path(__file__).resolve().parents[2]
file_handler = logging.FileHandler(f'{project_root}/logs/hosts.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)