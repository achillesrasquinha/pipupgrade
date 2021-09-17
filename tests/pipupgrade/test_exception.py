

<<<<<<< HEAD
# imports - module imports
from pipupgrade.exception import (
    PipupgradeError
=======
# imports - standard imports
import subprocess as sp

# imports - module imports
from bpyutils.util.system import popen
from pipupgrade.exception   import (
    PipupgradeError,
    PopenError
>>>>>>> template/master
)

# imports - test imports
import pytest

def test_pipupgrade_error():
    with pytest.raises(PipupgradeError):
<<<<<<< HEAD
        raise PipupgradeError
=======
        raise PipupgradeError

def test_popen_error():
    with pytest.raises(PopenError):
        popen('python -c "from pipupgrade.exceptions import PopenError; raise PopenError"')

    assert isinstance(
        PopenError(0, "echo foobar"),
        (PipupgradeError, sp.CalledProcessError)
    )
    assert isinstance(PipupgradeError(), Exception)
>>>>>>> template/master
