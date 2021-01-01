import os.path as osp

# imports - compatibility imports
from pipupgrade.commands    import _command as command
from pipupgrade.util._dict  import merge_dict

# imports - test imports
import pytest

# imports - test imports
from testutils import mock_input, PATH

def test_command_self(capfd):
    command(self = True, yes = True)
    out, err = capfd.readouterr()
    assert "upto date." in out

def test_command(capfd):
    command(verbose = True, yes = True, pip = True)