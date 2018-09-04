# imports - standard imports
import sys
from   contextlib import contextmanager

__STDIN__ = sys.stdin

@contextmanager
def mock_input(args):
    # https://stackoverflow.com/a/36491341
    sys.stdin = args
    yield
    sys.stdin = __STDIN__