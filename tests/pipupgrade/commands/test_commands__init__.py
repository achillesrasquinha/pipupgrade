# imports - compatibility imports
from pipupgrade._compat import StringIO

# imports - test imports
import pytest

# imports - module imports
from pipupgrade.commands import command

# imports - test imports
from tests.util import mock_input

def test_command():
    with mock_input(StringIO("Y")):
        command(check = True)

    with mock_input(StringIO("Y")):
        command()