# imports - compatibility imports
from pipupgrade._compat     import StringIO, input
from pipupgrade.util.string import safe_encode

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

def assert_stdout(capfd, output):
    stdout, _ = capfd.readouterr()
    assert output == safe_encode(stdout)

def assert_input(capfd, text, output, expected = None, input_ = None, stdout = None, input_args = { }):
    if expected == None:
        expected = output
    input_ = input_ or input
    stdout = stdout or text
    
    with mock_input(StringIO(output)):
        assert input_(text, *input_args) == expected
        assert_stdout(capfd, stdout)