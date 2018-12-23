# imports - compatibility imports
from pipupgrade._compat import StringIO

# imports - test imports
import pytest

# imports - module imports
from pipupgrade.commands   import command
from pipupgrade.util._test import mock_input

def test_command(capsys):
    with mock_input(StringIO("Y")):
        command(check = True)

    with mock_input(StringIO("Y")):
        command()