import functools
from time import time

from khostman.utils.utils import Utils


class LoggingUtils(Utils):
    """
    A class that provides utility methods for logging.
    """

    @staticmethod
    def timer(func):
        """
        A decorator function that measures the time it takes to execute a function.
        """

        @functools.wraps(func)
        def wrapper(*args):
            t1 = time()
            result = func(*args)
            t2 = time() - t1
            print(f'Execution of {func.__name__} took {t2} seconds')
            return result

        return wrapper

    @staticmethod
    def func_and_args_logging(func):
        """
        A decorator function that logs the start and finish of a function call along with its arguments.
        """
        from khostman.logger.logger import logger
        @functools.wraps(func)
        def wrapper(*args):
            logger.debug(f'[FUNCTION-START]\t{func.__name__}\t[ARGS]\t{str(args)[1:-1]}')
            result = func(*args)
            logger.debug(f'[FUNCTION-FINISH]\t{func.__name__}\t[ARGS]\t{str(args)[1:-1]}')
            return result

        return wrapper
