# imports - module imports
from pipupgrade.exception   import (
    PipupgradeError
)

# imports - test imports
import pytest

def test_pipupgrade_error():
    with pytest.raises(PipupgradeError):
        raise PipupgradeError