import os.path as osp

# imports - compatibility imports
from pipupgrade.commands  import _command as command
from bpyutils.util.string import strip_ansi
from bpyutils.config	  import get_config_path
from bpyutils.util.system import make_temp_dir, read
from pipupgrade.__attr__  import __name__ as NAME

def test_command_doctor(capfd):
    path_config = get_config_path(name = NAME)
    path_db     = osp.join(path_config, "db.db")
    
    assert osp.exists(path_db)
    command(verbose = True, doctor = True, clean = True)
    assert not osp.exists(path_db)

# TODO: pipupgrade --resolve

def test_command_file(capfd):
    with make_temp_dir() as tmp_dir:
        log_file = osp.join(tmp_dir, "logs.txt")
        
        assert not osp.exists(log_file)
        command(verbose = True, output = log_file, self = True)
        assert osp.exists(log_file)
        
        out, err = capfd.readouterr()
        assert strip_ansi(out) == read(log_file)

# TODO: pipupgrade --pip

def test_command_self(capfd):
    command(verbose = True, self = True, pip = True)
    out, err  = capfd.readouterr()
    sanitized = strip_ansi(out)

    # assert "pip upto date." in sanitized
    assert "pipupgrade upto date." in sanitized

# def test_command(capfd):
#     project      = osp.join(PATH["DATA"], "project")
#     requirements = osp.join(project, "requirements.txt")
#     pipfile      = osp.join(project, "Pipfile")

#     command(verbose = True, yes = True, pip = True, ignore_error = True)
#         requirements = requirements, pipfile = pipfile, ignore_error = True)
