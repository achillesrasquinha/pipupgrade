# imports - compatibility imports
from bpyutils.util.system import popen, pardir
from bpyutils.util.string import safe_decode
from bpyutils._compat     import StringIO, EX_OK, input

# imports - standard imports
import sys
import os.path as osp
from   contextlib import contextmanager
import traceback

PATH            = dict()
PATH["BASE"]    = pardir(__file__, 2)
PATH["DATA"]    = osp.join(PATH["BASE"], "data")

__STDIN__ = sys.stdin

@contextmanager
def mock_input(args):
    # https://stackoverflow.com/a/36491341
    sys.stdin = args
    yield
    sys.stdin = __STDIN__

def assert_stdout(capfd, output):
    stdout, _ = capfd.readouterr()
    assert safe_decode(output) == safe_decode(stdout)

def assert_input(capfd, text, output, expected = None, input_ = None, stdout = None, input_args = { }):
    if expected == None:
        expected = output
    input_ = input_ or input
    stdout = stdout or text
    
    with mock_input(StringIO(output)):
        assert input_(text, *input_args) == expected
        assert_stdout(capfd, stdout)

class CLIRunnerResult(object):
    pass

class Capture(object):
    def __enter__(self):
        self._stdout    = sys.stdout
        
        self._output    = StringIO()

        sys.stdout      = self._output

        return self
        
    def __exit__(self, *args):
        self.output     = safe_decode(self._output.getvalue())
        del self._output
        sys.stdout      = self._stdout

class CLIRunner(object):
    def invoke(self, command, args, **kwargs):
        code    = EX_OK
        error   = ""

        with Capture() as capture:
            try:
                command(**args)
            except Exception:
                code    = 1
                error   = traceback.format_exception()
        
        result          = CLIRunnerResult()

        result.code     = code
        result.output   = capture.output
        result.eror     = error

        return result