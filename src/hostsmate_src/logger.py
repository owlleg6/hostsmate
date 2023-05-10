import datetime
import logging
from pathlib import Path

import utils.os_utils as utils


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
        log_file: Path = self.get_logs_dir() / f'{datetime.date.today()}.log'

        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not self.has_file_handler(logger):
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s] - %(message)s')
            file_handler: logging.FileHandler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    @staticmethod
    def has_file_handler(logger: logging.Logger) -> bool:
        """
        Check whether a logger has a file handler already added.

        Args:
            logger (logging.Logger): The logger object.

        Returns:
            bool: True if a file handler has already been added, False otherwise.
        """
        return any(
            isinstance(handler, logging.FileHandler) for handler in logger.handlers
        )

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
