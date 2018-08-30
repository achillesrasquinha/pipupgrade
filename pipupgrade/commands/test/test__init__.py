# imports - compatibility imports
from pipupgrade._compat import builtins

# imports - test imports
import mock

# imports - module imports
from pipupgrade.commands import command

def test_command():
    with mock.patch.object(builtins, "input", lambda _: "Y"):
        assert command() == 0