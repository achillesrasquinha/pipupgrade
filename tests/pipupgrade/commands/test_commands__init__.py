<<<<<<< HEAD
# imports - compatibility imports
from pipupgrade.commands  import _command as command
from bpyutils.util.string import strip_ansi

def test_command_self(capfd):
    command(self = True, pip = True)
    out, err  = capfd.readouterr()
    sanitized = strip_ansi(out)

    # assert "pip upto date." in sanitized
    assert "pipupgrade upto date." in sanitized

# def test_command(capfd):
#     project      = osp.join(PATH["DATA"], "project")
#     requirements = osp.join(project, "requirements.txt")
#     pipfile      = osp.join(project, "Pipfile")

#     command(verbose = True, yes = True, pip = True, ignore_error = True)
        # requirements = requirements, pipfile = pipfile, ignore_error = True)
=======
import os.path as osp

# imports - compatibility imports
from pipupgrade.commands    import _command as command
from bpyutils.util._dict  import merge_dict
from bpyutils.util.string import strip_ansi

# imports - test imports
import pytest

# imports - test imports
from testutils import mock_input, PATH
>>>>>>> template/master
