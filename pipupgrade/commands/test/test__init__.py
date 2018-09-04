# imports - compatibility imports
from pipupgrade._compat import StringIO

# imports - module imports
from pipupgrade.commands  import command
from pipupgrade.util.test import mock_input

def test_command():
    with mock_input(StringIO("Y")):
        assert command() == 0
    pass