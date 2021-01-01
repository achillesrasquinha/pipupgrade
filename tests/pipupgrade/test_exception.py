# imports - standard imports
import subprocess as sp

# imports - module imports
from pipupgrade.util.system import popen
from pipupgrade.exception   import (
    PipupgradeError,
    PopenError
)

# imports - test imports
import pytest

def test_pipupgrade_error():
    with pytest.raises(PipupgradeError):
        raise PipupgradeError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "raise TypeError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (PipupgradeError, sp.CalledProcessError)
    )
    assert isinstance(PipupgradeError(), Exception)