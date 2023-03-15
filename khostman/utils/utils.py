import sys
from tempfile import gettempdir
from uuid import uuid4
from os.path import join
from os import getuid
import ctypes
import functools
from time import time
from pathlib import Path


def is_root():
    try:
        root = getuid() == 0
    except AttributeError:
        root = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not root:
        sys.exit('Please run the application as a '
                 'root/administrator to edit the Hosts file.')


def get_platform():
    platform = sys.platform
    if platform.startswith('linux') \
            or platform.startswith('darwin') \
            or platform.startswith('freebsd'):
        return 'unix_like'
    elif platform.startswith('win'):
        return 'windows'


def path_to_hosts() -> Path:
    platform = get_platform()
    if platform == 'unix_like':
        hosts_path = Path('/etc/hosts')
        return hosts_path
    elif platform == 'windows':
        root_drive = Path(sys.executable).anchor
        hosts_path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')
        return hosts_path


def timer(func):
    @functools.wraps(func)
    def wrapper(*args):
        t1 = time()
        result = func(*args)
        t2 = time() - t1
        print(f'Execution of {func.__name__} took {t2} seconds')
        return result

    return wrapper


def func_and_args_logging(func):
    from khostman.logger.logger import logger
    @functools.wraps(func)
    def wrapper(*args):
        logger.debug(f'[FUNCTION-START]\t{func.__name__}\t[ARGS]\t{str(args)[1:-1]}')
        result = func(*args)
        logger.debug(f'[FUNCTION-FINISH]\t{func.__name__}\t[ARGS]\t{str(args)[1:-1]}')
        return result

    return wrapper


@func_and_args_logging
def mk_tmp_hex_file():
    """
    Creates a temporary file with unique hexadecimal name in the system's temporary directory
    """
    tmp = join(gettempdir(), uuid4().hex)
    return tmp
