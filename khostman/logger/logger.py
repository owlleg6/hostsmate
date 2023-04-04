import logging
from pathlib import Path

import khostman.utils.os_utils as utils


class HostsLogger:
    """
    This class is used to create Logger instances.
    """

    def create_logger(self, name: str) -> logging.Logger:
        """
        Create a logger object and return it.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger: The logger object.
        """
        logs_dir: Path = self.get_logs_dir()

        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] '
                                      '[%(name)s.%(funcName)s] - %(message)s')

        file_handler = logging.FileHandler(f'{logs_dir}/hosts.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_logs_dir() -> Path:
        """
        Return the path to the directory where the log files will be stored.

        Returns:
            Path: The path to the logs directory.
        """
        logs_dir: Path = utils.OSUtils.get_project_root() / 'logs'

        if not logs_dir.exists():
            logs_dir.mkdir()
        return logs_dir
